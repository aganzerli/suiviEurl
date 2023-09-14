# coding: latin-1

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle

import database as db
import utils

'''standardFonts = (
'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
'Symbol','ZapfDingbats')'''


# ----------------------------------------------------------------------------------------------------------------------------------
def generate(creance, entreprise, client) :
    if not ( creance and entreprise and client ) :
        return False

    intitule= creance.getParam("intitule")
    objet= creance.getParam("objet")
    montant= creance.getParam("montant")
    montantTtc= creance.getParam("montantTtc")
    tva= creance.getParam("tva")
    date= creance.getParam("date")
    factureno= creance.getParam("factureno")
    echeance= "A réception" if creance.getParam("delai") == db.DELAI_ARECEPTION else creance.getParam("echeance").strftime("%d/%m/%Y")

    nom= entreprise.getParam("nom")
    adresse1= entreprise.getParam("adresse1")
    adresse2= entreprise.getParam("adresse2")
    capital= entreprise.getParam("capital")
    siret= entreprise.getParam("siret")
    numero_rcs= entreprise.getParam("numero_rcs")
    ville_rcs= entreprise.getParam("ville_rcs")
    numero_tva= entreprise.getParam("numero_tva")
    banque= entreprise.getParam("banque")
    iban= entreprise.getParam("iban")
    bicswift= entreprise.getParam("bicswift")

    client_nom= client.getParam("nom")
    client_adresse1= client.getParam("adresse1")
    client_adresse2= client.getParam("adresse2")

    path= "{0}/{1}/{2:02d}{3:02d}/{4}.pdf".format(db.INVOICE_FOLDER, date.year, date.month, date.day, factureno)

    utils.createFolder(os.path.dirname(path))

    # create a Canvas object with a filename
    doc= SimpleDocTemplate(path,
        pagesize= A4,
        leftMargin= 2.0*cm,
        rightMargin= 2.0*cm,
        topMargin= 1.5*cm,
        bottomMargin= 1.5*cm)

    width= doc.width
    height= doc.height
    header1Height= height*0.05
    header2Height= height*0.1
    footer1Height= height*0.1
    footer2Height= height*0.05
    spacing= 1.5*cm

    tableWidth= width*0.8
    tableHeight= height-(header1Height+header2Height+footer1Height+footer2Height+4.0*spacing+0.5*cm)
    cellHeight= tableHeight/21.0
    leading= 0.95*cellHeight

    elements = []

    # header1
    data= [
        [client_nom],
        ["Facture n. {0}".format(factureno)]
        ]
    style= TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEADING",(0,0),(-1,-1),leading),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),11),
        ("ALIGN",(0,0),(-1,-1),"RIGHT"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")
        ])
    header1Table= Table(data, [width*0.33333], 2*[cellHeight], style= style)

    data= [
        [nom, header1Table]
        ]
    style= TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEADING",(0,0),(-1,-1),leading),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),24),
        ("ALIGN",(0,0),(0,0),"LEFT"),
        ("ALIGN",(1,0),(1,0),"RIGHT"),
        ("VALIGN",(0,0),(-1,-1),"TOP")
        ])
    header1= Table(data, [width*0.66666, width*0.33333], [2*cellHeight], style= style)

    # header2
    data= [
        [client_nom],
        [client_adresse1],
        [client_adresse2]
        ]
    style= TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEADING",(0,0),(-1,-1),leading),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("FONTNAME",(0,0),(0,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),11),
        ("ALIGN",(0,0),(-1,-1),"RIGHT"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE")
        ])
    header2= Table(data, [width], 3*[cellHeight], style= style)

    # table
    data= [
        [intitule,                  ""], # 0
        ["",                        ""], # 1
        ["",                        ""], # 2
        ["DESCRIPTION",             "TOTAL"], # 3
        ["",                        ""], # 4
        [objet,                     "{0} \N{euro sign}".format(montant)], # 5
        ["",                        ""], # 6
        ["total HT",                "{0} \N{euro sign}".format(montant)], # 7
        ["",                        ""], # 8
        ["TVA {0}%".format(tva),    "{0} \N{euro sign}".format(utils.roundUp(montantTtc-montant, 2))], # 9
        ["",                        ""], # 10
        ["TOTAL TTC",               "{0} \N{euro sign}".format(montantTtc)], # 11
        ["",                        ""], # 12
        ["",                        ""], # 13
        ["date de la facture :",    date.strftime("%d/%m/%Y")], # 14
        ["échéance de paiement :",  echeance], # 15
        ["",                        ""], # 16
        ["",                        ""], # 17
        ["BANQUE : {0}".format(banque),                ""], # 18
        ["IBAN : {0}".format(iban),           ""], # 19
        ["BIC/SWIFT : {0}".format(bicswift),       ""] # 20
        ]
    style= TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),3),
        ("RIGHTPADDING",(0,0),(-1,-1),3),
        ("TOPPADDING",(0,0),(-1,-1),3),
        ("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEADING",(0,0),(-1,-1),leading),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTNAME",(0,3),(-1,3),"Helvetica-Bold"),
        ("FONTNAME",(0,11),(-1,11),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),11),
        ("FONTSIZE",(0,3),(-1,3),13),
        ("FONTSIZE",(0,11),(-1,11),13),
        ("ALIGN",(0,0),(0,-1),"LEFT"),
        ("ALIGN",(1,0),(1,-1),"RIGHT"),
        ("ALIGN",(0,14),(0,15),"RIGHT"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("BOX", (0,5), (-1,7), 0.25, colors.black),
        ("LINEAFTER", (0,5), (0,7), 0.25, colors.black),
        ("GRID", (0,11), (-1,11), 0.25, colors.black)
        ])
    table= Table(data, [tableWidth*0.66666, tableWidth*0.33333], 21*[cellHeight], style= style)

    # footer1
    footer1Text= "Tout paiement de facture par chèques doit être libellés à l'ordre de {0}\n\
    Nous vous informons que les factures seront payable sous 30 jours. Les factures d'acompte sont payable a reception.\n\
    Aucun escompte pour paiement anticipé. Pénalités de retard au taux de 12% annuels.\n\
    {0} se réserve la propriété des biens et contenus jusqu'au complet paiement de l'ensemble des factures.\n\
    Cette revendication porte aussi bien sur les marchandises et contenus que sur leur valeur si elle ont été revendues (Loi 80-335 du 12 mai 1980)".format(nom)
    footer1Style= ParagraphStyle("headerstyle", fontName= "Helvetica", fontSize= 7, alignment= 0)
    footer1= Paragraph(footer1Text.replace("\n", "<br />"), footer1Style)

    # footer2
    footer2Text= "{0} - {1} {2}\n\
        EURL au Capital de {3} EUROS - R.C.S. {4} {5} - Siret {6} - TVA intra {7}".format(nom, adresse1, adresse2, capital, ville_rcs, numero_rcs, siret, numero_tva)
    footer2Style= ParagraphStyle("headerstyle", fontName= "Helvetica", fontSize= 7, alignment= 1)
    footer2= Paragraph(footer2Text.replace("\n", "<br />"), footer2Style)

    # main
    data= [
        [header1],  # header1
        [""],       # spacing
        [header2],  # header2
        [""],       # spacing
        [table],    # table
        [""],       # spacing
        [footer1],  # footer1
        [""],       # spacing
        [footer2],  # footer2
        ]
    style= TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),
        ("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEADING",(0,0),(-1,-1),leading),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("VALIGN",(0,6),(-1,6),"MIDDLE"),
        ("VALIGN",(0,8),(-1,8),"BOTTOM"),
        #("GRID", (0,0), (-1,-1), 0.25, colors.red)
        ])
    main= Table(data, 1*[width], [header1Height, spacing, header2Height, spacing, tableHeight, spacing, footer1Height, spacing, footer2Height], style= style)
    elements.append(main)

    doc.build(elements)

    return path
