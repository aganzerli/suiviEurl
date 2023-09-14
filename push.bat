rem git init
rem git remote add sources https://login:password@github.com/aganzerli/sources.git


@ECHO OFF


ECHO Syncing with repository...
ECHO ===============================================================================


D:
CD D:\Alpha Site\suiviEurl

git pull suiviEurl master
git status

CHOICE /C YN
IF ERRORLEVEL==2 GOTO __end

git add -A
git commit -m "commit %USERNAME%"

CHOICE /C YN
IF ERRORLEVEL==2 GOTO __end

git push suiviEurl master


PAUSE


:__end
@ECHO ON
@EXIT /B 0