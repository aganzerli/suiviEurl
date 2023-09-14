# coding: latin-1


import datetime
import math
import json
import os
import copy
import weakref

import utils

#ROOT_FOLDER= "{0}/suiviEurl".format(utils.userFolder())
ROOT_FOLDER= "{0}/data".format(os.getcwd())
DATABASE_FOLDER= "{0}/database".format(ROOT_FOLDER)
DATABASE_BACKUPFOLDER= "{0}/backup".format(DATABASE_FOLDER)
DATABASE_PATH= "{0}/database.json".format(DATABASE_FOLDER)
INVOICE_FOLDER= "{0}/factures".format(ROOT_FOLDER)

DELAI_ARECEPTION= 0
DELAI_30J= 1
DELAI_60J= 2
DELAI_STR= ["A réception", "30 jours", "60 jours"]

STATUT_PREVISION= 0
STATUT_ENCOURS= 1
STATUT_PAYE= 2
STATUT_ANNULE= 3
STATUT_STR= ["Prévision", "En cours", "Payé", "Annulé"]

OCCURENCE_MOIS= 0
OCCURENCE_ANNEE= 1
OCCURENCE_PONCTUEL= 2
OCCURENCE_STR= ["Au mois", "A l'année", "Ponctuel"]

MONTHS= ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novenmbre", "Décembre"]


# ==================================================================================================================================
class BaseObject(object) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return {}

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, params) :
        self.m_params= params
        self.m_parent= weakref.ref(parent) if parent else None

    # ------------------------------------------------------------------------------------------------------------------------------
    def compute(self) :
        return

    # ------------------------------------------------------------------------------------------------------------------------------
    def setParam(self, key, value) :
        if key in self.m_params :
            self.m_params[key]= value

    # ------------------------------------------------------------------------------------------------------------------------------
    def getParam(self, key, default= None) :
        return self.m_params.get(key, default)

    # ------------------------------------------------------------------------------------------------------------------------------
    def serialize(self) :
        return self.m_params

    # ------------------------------------------------------------------------------------------------------------------------------
    def unserialize(self, data) :
        self.m_params= self.defaultParams()
        self.m_params.update(data)

    # ------------------------------------------------------------------------------------------------------------------------------
    def parent(self) :
        return self.m_parent() if self.m_parent else None


# ==================================================================================================================================
class Item(BaseObject) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return {
            "nom" : "",
            "intitule" : "",
            "objet" : "",
            "montant" : 0.0,
            "montantTtc" : None,
            "tva" : 20.0,
            "statut" : STATUT_PREVISION,
            "factureno" : "",
            "date" : datetime.date.today(),
            "delai" : DELAI_ARECEPTION,
            "echeance" : None,
            "datePaiement" : None,
            "modalites" : None,
            "occurence" : OCCURENCE_PONCTUEL
            }

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Item, self).__init__(parent, self.defaultParams())

    # ------------------------------------------------------------------------------------------------------------------------------
    def setParam(self, key, value) :
        if key == "montant" :
            super(Item, self).setParam("montant", utils.roundUp(value, 2) if value is not None else None)
            super(Item, self).setParam("montantTtc", None)
        elif key == "montantTtc" :
            super(Item, self).setParam("montant", None)
            super(Item, self).setParam("montantTtc", utils.roundUp(value, 2) if value is not None else None)
        elif key == "tva" :
            super(Item, self).setParam("tva", utils.roundUp(value, 2) if value is not None else 0.0)
        elif key == "statut" :
            super(Item, self).setParam("statut", value)
            if ( value == STATUT_PREVISION ) or ( value == STATUT_ENCOURS ) or ( value == STATUT_ANNULE ) :
                super(Item, self).setParam("datePaiement", None)
                super(Item, self).setParam("modalites", None)
            elif ( value == STATUT_PAYE ) :
                super(Item, self).setParam("datePaiement", datetime.date.today())
                super(Item, self).setParam("modalites", "")
        else :
            super(Item, self).setParam(key, value)

    # ------------------------------------------------------------------------------------------------------------------------------
    def compute(self) :
        date= self.getParam("date") # compute 'echeance'
        delai= self.getParam("delai")

        if delai == DELAI_ARECEPTION :
            echeance= date
        elif delai == DELAI_30J :
            echeance= date+datetime.timedelta(days=30)
        else :
            echeance= date+datetime.timedelta(days=60)
        super(Item, self).setParam("echeance", echeance)

        montant= self.getParam("montant")  # compute 'montant' or 'montantTtc'
        montantTtc= self.getParam("montantTtc")
        if ( montant is None ) and ( montantTtc is None ) :
            return

        tva= self.getParam("tva", default= 0.0)

        if montant is not None :
            tva_= utils.roundUp(montant*(tva/100.0), 2)
            montantTtc= utils.roundUp(montant+tva_, 2)
            super(Item, self).setParam("montantTtc", montantTtc)

        elif montantTtc is not None :
            tva_= utils.roundUp(montantTtc*(1.0-1.0/(1.0+tva/100.0)), 2)
            montant= utils.roundUp(montantTtc-tva_, 2)
            super(Item, self).setParam("montant", montant)

    # ------------------------------------------------------------------------------------------------------------------------------
    def serialize(self) :
        data= {}
        for key, value in self.m_params.items() :
            if ( ( key == "date" ) or ( key == "echeance" ) or ( key == "datePaiement" ) ) and value :
                data[key]= (value.year, value.month, value.day)
            else :
                data[key]= value

        return data

    # ------------------------------------------------------------------------------------------------------------------------------
    def unserialize(self, data) :
        params= self.defaultParams()
        for key, value in data.items() :
            if ( ( key == "date" ) or ( key == "echeance" ) or ( key == "datePaiement" ) ) and value :
                params[key]= datetime.date(value[0], value[1], value[2])
            else :
                params[key]= value

        self.m_params= params


# ==================================================================================================================================
class Year(BaseObject) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return {
            "annee" : 0,

            "creances" : [],
            "creances_parMois" : [0.0]*len(MONTHS),
            "creances_parMoisTtc" : [0.0]*len(MONTHS),
            "creances_totalPonctuel" : 0.0,
            "creances_totalPonctuelTtc" : 0.0,
            "creances_totalMois" : 0.0,
            "creances_totalMoisTtc" : 0.0,
            "creances_totalAnnee" : 0.0,
            "creances_totalAnneeTtc" : 0.0,
            "creances_total" : 0.0,
            "creances_totalTtc" : 0.0,

            "salaires" : [],
            "salaires_parMois" : [0.0]*len(MONTHS),
            "salaires_parMoisTtc" : [0.0]*len(MONTHS),
            "salaires_totalPonctuel" : 0.0,
            "salaires_totalPonctuelTtc" : 0.0,
            "salaires_totalMois" : 0.0,
            "salaires_totalMoisTtc" : 0.0,
            "salaires_totalAnnee" : 0.0,
            "salaires_totalAnneeTtc" : 0.0,
            "salaires_total" : 0.0,
            "salaires_totalTtc" : 0.0,

            "dettes" : [],
            "dettes_parMois" : [0.0]*len(MONTHS),
            "dettes_parMoisTtc" : [0.0]*len(MONTHS),
            "dettes_totalPonctuel" : 0.0,
            "dettes_totalPonctuelTtc" : 0.0,
            "dettes_totalMois" : 0.0,
            "dettes_totalMoisTtc" : 0.0,
            "dettes_totalAnnee" : 0.0,
            "dettes_totalAnneeTtc" : 0.0,
            "dettes_total" : 0.0,
            "dettes_totalTtc" : 0.0,

            "fraisFixes" : [],
            "fraisFixes_parMois" : [0.0]*len(MONTHS),
            "fraisFixes_parMoisTtc" : [0.0]*len(MONTHS),
            "fraisFixes_totalPonctuel" : 0.0,
            "fraisFixes_totalPonctuelTtc" : 0.0,
            "fraisFixes_totalMois" : 0.0,
            "fraisFixes_totalMoisTtc" : 0.0,
            "fraisFixes_totalAnnee" : 0.0,
            "fraisFixes_totalAnneeTtc" : 0.0,
            "fraisFixes_total" : 0.0,
            "fraisFixes_totalTtc" : 0.0,

            "cotisations" : [],
            "cotisations_parMois" : [0.0]*len(MONTHS),
            "cotisations_parMoisTtc" : [0.0]*len(MONTHS),
            "cotisations_totalPonctuel" : 0.0,
            "cotisations_totalPonctuelTtc" : 0.0,
            "cotisations_totalMois" : 0.0,
            "cotisations_totalMoisTtc" : 0.0,
            "cotisations_totalAnnee" : 0.0,
            "cotisations_totalAnneeTtc" : 0.0,
            "cotisations_total" : 0.0,
            "cotisations_totalTtc" : 0.0,

            "bilanEst_parMois" : [0.0]*len(MONTHS),
            "bilan_parMois" : [0.0]*len(MONTHS),

            "plafond_ss" : 43992.0,
            "maladie_maternite" : 0.0,
            "maladie_indemnite" : 0.0,
            "allocations_familiales" : 0.0,
            "formation_professionnelle" : 110.0,
            "retraite_de_base" : 0.0,
            "retraite_complementaire" : 0.0,
            "invalidite_deces" : 0.0,
            "csg_crds" : 0.0,
            "total_urssaf" : 0.0,
            "taux_sur_salaire_net" : 0.0,
            "taux_sur_total" : 0.0,

            "total_entrees" : 0.0,
            "total_sorties" : 0.0,
            "balance" : 0.0
            }

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Year, self).__init__(parent, self.defaultParams())

    # ------------------------------------------------------------------------------------------------------------------------------
    def compute(self) :
        self._compute_table(["creances", "dettes", "fraisFixes", "salaires", "cotisations"])

        creances_parMois= self.getParam("creances_parMois")
        dettes_parMois= self.getParam("dettes_parMois")
        fraisFixes_parMois= self.getParam("fraisFixes_parMois")
        salaires_parMois= self.getParam("salaires_parMois")
        salaires_annee= self.getParam("salaires_total")
        plafond_ss= self.getParam("plafond_ss")
        formation_professionnelle= self.getParam("formation_professionnelle")

        bilanEst_parMois= [0.0]*len(MONTHS)
        for i in range(len(MONTHS)) :
            bilanEst_parMois[i]= utils.roundUp(creances_parMois[i]-(dettes_parMois[i]+fraisFixes_parMois[i]+salaires_parMois[i]), 2)
        self.setParam("bilanEst_parMois", bilanEst_parMois)

        bilan_parMois= [0.0]*len(MONTHS)
        bilan_parMois[0]= bilanEst_parMois[0]
        for i in range(1, len(MONTHS)) :
            bilan_parMois[i]= utils.roundUp(bilan_parMois[i-1]+bilanEst_parMois[i], 2)
        self.setParam("bilan_parMois", bilan_parMois)

        maladie_maternite= utils.roundUp(salaires_annee*6.35/100.0)
        self.setParam("maladie_maternite", maladie_maternite)

        maladie_indemnite= utils.roundUp(salaires_annee*0.0085)
        self.setParam("maladie_indemnite", maladie_indemnite)

        if salaires_annee < plafond_ss*1.1 :
            allocations_familiales= 0.0
        else :
            if salaires_annee < plafond_ss*1.4 :
                allocations_familiales= salaires_annee*3.1/100.0
            else :
                allocations_familiales= salaires_annee*3.1/100.0
        allocations_familiales= utils.roundUp(allocations_familiales)
        self.setParam("allocations_familiales", allocations_familiales)

        if salaires_annee < plafond_ss :
            retraite_de_base= salaires_annee*8.23/100.0
        else :
            retraite_de_base= plafond_ss*8.23/100.0+salaires_annee*1.87/100.0
        retraite_de_base= utils.roundUp(retraite_de_base)
        self.setParam("retraite_de_base", retraite_de_base)

        if salaires_annee < plafond_ss :
            retraite_complementaire= salaires_annee*9.0/100.0
        else :
            retraite_complementaire= plafond_ss*9.0/100.0+(salaires_annee-plafond_ss)*22.0/100.0
        retraite_complementaire= utils.roundUp(retraite_complementaire)
        self.setParam("retraite_complementaire", retraite_complementaire)

        if salaires_annee < plafond_ss :
            invalidite_deces= salaires_annee*0.25/100.0
        else :
            invalidite_deces= salaires_annee*0.5/100.0
        invalidite_deces= utils.roundUp(invalidite_deces)
        self.setParam("invalidite_deces", invalidite_deces)

        total_urssaf= maladie_maternite+maladie_indemnite+allocations_familiales+formation_professionnelle+retraite_de_base+retraite_complementaire+invalidite_deces

        csg_crds= utils.roundUp((salaires_annee+total_urssaf)*0.097)
        self.setParam("csg_crds", csg_crds)

        total_urssaf+= csg_crds
        self.setParam("total_urssaf", total_urssaf)

        if salaires_annee > 0.0 :
            taux_sur_salaire_net= total_urssaf/salaires_annee
        else :
            taux_sur_salaire_net= 0.0
        taux_sur_salaire_net= float(round(100.0*taux_sur_salaire_net))
        self.setParam("taux_sur_salaire_net", taux_sur_salaire_net)

        if salaires_annee > 0.0 :
            taux_sur_total= total_urssaf/(total_urssaf+salaires_annee)
        else :
            taux_sur_total= 0.0
        taux_sur_total= float(round(100.0*taux_sur_total))
        self.setParam("taux_sur_total", taux_sur_total)

        total_entrees= self.getParam("creances_total")
        self.setParam("total_entrees", total_entrees)

        total_sorties= utils.roundUp(self.getParam("dettes_total")+self.getParam("fraisFixes_total")+self.getParam("salaires_total")+total_urssaf, 2)
        self.setParam("total_sorties", total_sorties)

        balance= utils.roundUp(total_entrees-total_sorties, 2)
        self.setParam("balance", balance)

    # ------------------------------------------------------------------------------------------------------------------------------
    def _compute_table(self, tableName) :
        if not isinstance(tableName, list) :
            tableName= [tableName]

        for tn in tableName :
            table= self.getParam(tn)
            if table is not None :
                table.sort(key= lambda x : x.getParam("date"))

                for item in table :
                    item.compute()

                parMois= [0.0]*len(MONTHS)
                parMoisTtc= [0.0]*len(MONTHS)
                totalPonctuel= 0.0
                totalPonctuelTtc= 0.0
                totalMois= 0.0
                totalMoisTtc= 0.0
                totalAnnee= 0.0
                totalAnneeTtc= 0.0

                for item in table :
                    statut= item.getParam("statut")
                    if statut != STATUT_ANNULE :
                        montant= item.getParam("montant")
                        montantTtc= item.getParam("montantTtc")
                        if montant and montantTtc :
                            occurence= item.getParam("occurence", default= OCCURENCE_PONCTUEL)

                            if occurence == OCCURENCE_PONCTUEL :
                                date= item.getParam("date")
                                if date :
                                    parMois[date.month-1]+= montant
                                    parMoisTtc[date.month-1]+= montantTtc
                                    totalPonctuel+= montant
                                    totalPonctuelTtc+= montantTtc

                            elif occurence == OCCURENCE_MOIS :
                                for i in range(len(MONTHS)) :
                                    parMois[i]+= montant
                                    parMoisTtc[i]+= montantTtc
                                totalMois+= montant
                                totalMoisTtc+= montantTtc

                            elif occurence == OCCURENCE_ANNEE :
                                parMois[11]+= montant
                                parMoisTtc[11]+= montantTtc
                                totalAnnee+= montant
                                totalAnneeTtc+= montantTtc

                self.setParam(tn+"_parMois", [ utils.roundUp(i, 2) for i in parMois ])
                self.setParam(tn+"_parMoisTtc", [ utils.roundUp(i, 2) for i in parMoisTtc ])
                self.setParam(tn+"_totalPonctuel", utils.roundUp(totalPonctuel, 2))
                self.setParam(tn+"_totalPonctuelTtc", utils.roundUp(totalPonctuelTtc, 2))
                self.setParam(tn+"_totalMois", utils.roundUp(totalMois, 2))
                self.setParam(tn+"_totalMoisTtc", utils.roundUp(totalMoisTtc, 2))
                self.setParam(tn+"_totalAnnee", utils.roundUp(totalAnnee, 2))
                self.setParam(tn+"_totalAnneeTtc", utils.roundUp(totalAnneeTtc, 2))
                self.setParam(tn+"_total", utils.roundUp(sum(parMois), 2))
                self.setParam(tn+"_totalTtc", utils.roundUp(sum(parMoisTtc), 2))

    # ------------------------------------------------------------------------------------------------------------------------------
    def item(self, tableName, index) :
        item= None

        table= self.getParam(tableName)
        if table is not None :
            item= table[index]

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def addItem(self, tableName) :
        item= None

        table= self.getParam(tableName)
        if table is not None :
            item= Item(self)

            if tableName == "creances" :
                item.setParam("intitule", self.parent().getParam("intitule_default"))
                item.setParam("objet", self.parent().getParam("objet_default"))

            elif tableName == "fraisFixes" :
                item.setParam("occurence", OCCURENCE_MOIS)

            table.append(item)

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def removeItem(self, tableName, index) :
        table= self.getParam(tableName)
        if table is not None :
            table.pop(index)

    # ------------------------------------------------------------------------------------------------------------------------------
    def serialize(self) :
        data= {}
        for key, value in self.m_params.items() :
            if ( key == "creances" ) or ( key == "salaires" ) or ( key == "dettes" ) or ( key == "fraisFixes" ) or ( key == "cotisations" ) :
                data[key]= [ i.serialize() for i in value ]
            else :
                data[key]= value

        return data

    # ------------------------------------------------------------------------------------------------------------------------------
    def unserialize(self, data) :
        params= self.defaultParams()

        for key, value in data.items() :
            if ( key == "creances" ) or ( key == "salaires" ) or ( key == "dettes" ) or ( key == "fraisFixes" ) or ( key == "cotisations" ) :
                table= []
                for v in value :
                    item= Item(self)
                    item.unserialize(v)
                    table.append(item)
                params[key]= table
            else :
                params[key]= value

        self.m_params= params


# ==================================================================================================================================
class Entreprise(BaseObject) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return{
            "nom" : "",
            "adresse1" : "",
            "adresse2" : "",
            "capital" : 0.0,
            "siren" : "",
            "siret" : "",
            "numero_rcs" : "",
            "ville_rcs" : "",
            "numero_tva" : "",
            "banque" : "",
            "iban" : "",
            "bicswift" : ""
            }

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Entreprise, self).__init__(parent, self.defaultParams())


# ==================================================================================================================================
class Client(BaseObject) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return {
            "nom" : "",
            "adresse1" : "",
            "adresse2" : ""
            }

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent) :
        super(Client, self).__init__(parent, self.defaultParams())


# ==================================================================================================================================
class Database(BaseObject) :
    # ------------------------------------------------------------------------------------------------------------------------------
    def defaultParams(self) :
        return {
            "entreprise" : Entreprise(self),
            "clients" : [],
            "annees" : [],
            "intitule_default" : "Facture pour travaux de production",
            "objet_default" : ""
            }

    # ------------------------------------------------------------------------------------------------------------------------------
    def __init__(self) :
        super(Database, self).__init__(None, self.defaultParams())

    # ------------------------------------------------------------------------------------------------------------------------------
    def compute(self) :
        annees= self.getParam("annees")

        annees.sort(key= lambda x : x.getParam("annee"))

        for a in annees :
            a.compute()

    # ------------------------------------------------------------------------------------------------------------------------------
    def entreprise(self) :
        return self.getParam("entreprise")

    # ------------------------------------------------------------------------------------------------------------------------------
    def clients(self) :
        result= []

        for a in self.getParam("clients") :
            result.append(a.getParam("nom"))

        return result

    # ------------------------------------------------------------------------------------------------------------------------------
    def client(self, name) :
        item= None

        for a in self.getParam("clients") :
            if a.getParam("nom") == name :
                item= a
                break

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def addClient(self, name) :
        item= self.client(name)

        if item is None :
            item= Client(self)
            item.setParam("nom", name)

            self.getParam("clients").append(item)

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def removeClient(self, name) :
        for a in self.getParam("annees") :
            for c in a.getParam("creances") :
                if c.getParam("nom") == name :
                    return False

        clients= self.getParam("clients")

        for i in range(len(clients)) :
            if clients[i].getParam("nom") == name :
                clients.pop(i)
                return True

        return False

    # ------------------------------------------------------------------------------------------------------------------------------
    def years(self) :
        result= []

        for a in self.getParam("annees") :
            result.append(a.getParam("annee"))

        return result

    # ------------------------------------------------------------------------------------------------------------------------------
    def year(self, year) :
        if not year :
            year= 0
        year= int(year)

        item= None

        for a in self.getParam("annees") :
            if a.getParam("annee") == year :
                item= a
                break

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def addYear(self, year) :
        if not year :
            year= 0
        year= int(year)

        item= self.year(year)

        if item is None :
            item= Year(self)
            item.setParam("annee", year)

            self.getParam("annees").append(item)

        return item

    # ------------------------------------------------------------------------------------------------------------------------------
    def removeYear(self, year) :
        if not year :
            year= 0
        year= int(year)

        annees= self.getParam("annees")

        for i in range(len(annees)) :
            if annees[i].getParam("annee") == year :
                annees.pop(i)
                return True

        return False

    # ------------------------------------------------------------------------------------------------------------------------------
    def serialize(self) :
        data= {}
        for key, value in self.m_params.items() :
            if key == "entreprise" :
                data[key]= value.serialize()
            elif key == "clients" :
                data[key]= [ i.serialize() for i in value ]
            elif key == "annees" :
                data[key]= [ i.serialize() for i in value ]
            else :
                data[key]= value

        return data

    # ------------------------------------------------------------------------------------------------------------------------------
    def unserialize(self, data) :
        params= self.defaultParams()

        for key, value in data.items() :
            if key == "entreprise" :
                item= Entreprise(self)
                item.unserialize(value)
                params[key]= item
            elif key == "clients" :
                table= []
                for v in value :
                    item= Client(self)
                    item.unserialize(v)
                    table.append(item)
                params[key]= table
            elif key == "annees" :
                table= []
                for v in value :
                    item= Year(self)
                    item.unserialize(v)
                    table.append(item)
                params[key]= table
            else :
                params[key]= value

        self.m_params= params

    # ------------------------------------------------------------------------------------------------------------------------------
    def save(self) :
        backupPath= "{0}/{1}.json".format(DATABASE_BACKUPFOLDER, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        print("Copying backup {0}".format(backupPath))
        utils.copyFile(backupPath, DATABASE_PATH)

        self.compute()

        print("Saving {0}".format(DATABASE_PATH))
        data= self.serialize()
        data= json.dumps(data, indent= 3)
        utils.writeFile(DATABASE_PATH, data)

    # ------------------------------------------------------------------------------------------------------------------------------
    def load(self) :
        print("Loading {0}".format(DATABASE_PATH))
        data= utils.readFile(DATABASE_PATH)
        if data :
            data= json.loads(data)
            self.unserialize(data)

        self.compute()

