# DA-Placer
_Data-aware application placement and routing   in the Cloud-IoT continuum_

## Files &nbsp;<img src="https://cdn-icons-png.flaticon.com/512/149/149337.png" alt="files" width="20" height="20"/>
 - `model.pl` contains the way to describe the application and the infrastructure on which you want to attempt the placement and routing process.

 - `app.pl` and `infrastructure.pl` files contain an instance of the model.

 - `daplacer.pl` contains the main logic of the placer (&sime;140 lines of code).

## Tutorial &nbsp;<img src="https://cdn-icons-png.flaticon.com/512/3208/3208615.png" alt="checklist" width="20" height="20"/> 

1. Download or clone this repo.

2. In the project folder, run the following command on terminal, to access the [SWI-Prolog](https://www.swi-prolog.org/download/stable) console:
    ```console
    swipl daplacer.pl
    ```

3. Inside the console, run the following query:
    ```prolog
    :- daplacer(museuMonitor, Placement, Routes).
    ```
    The output will be a first placement and routing for the application described in `app.pl` (named _museuMonitor_), onto the infrastructure described in `infrastructure.pl`.

4. To try the _continuous reasoning_, open `infrastructure.pl` file and change some links or nodes involved in the first placement, or change `app.pl` description, adding new services, data types or end-to-end interactions.

4. Repeat _step 2_, and you'll obtain as output a new placement for new and suffering services.

### Output Example &nbsp;<img src="https://cdn-icons-png.flaticon.com/512/570/570162.png" alt="output" width="20" height="20"/> 

```prolog
% on(Service, Node)
Placement = [on(dataStorage, isp), 
             on(controller, lifeSciences), 
             on(interface, mannLab)],
```
```prolog
% ((source, target), AllocatedBandwidth, Route)
Routes = [((rVst, dataStorage), 24.0, [sciencesLectureHall, briggsHall, mannLab, parkingServices, westEntry, firePolice, isp]),  
          ((rArt, dataStorage), 15.0, [kleiberHall, hoaglandAnnex, firePolice, isp]),  
          ((dataStorage, controller), 18.0, [isp, firePolice, westEntry, mannLab, lifeSciences]),  
          ((controller, rDor), 22.5, [lifeSciences, parkingServices]),  
          ((controller, rGls), 27.0, [lifeSciences, parkingServices, mannLab, briggsHall, studentCenter]),  
          ((rCam, interface), 40, [hoaglandAnnex, mannLab]),  
          ((interface, controller), 40, [mannLab, westEntry, parkingServices, lifeSciences]),  
          ((interface, rVid), 20, [mannLab, parkingServices, westEntry])]
```

## Contributors <img src="https://cdn-icons-png.flaticon.com/512/33/33308.png" alt="output" width="20" height="20"/> 

 - [Jacopo Massa](http://pages.di.unipi.it/massa)
 - [Stefano Forti](http://pages.di.unipi.it/forti)
 - [Antonio Brogi](http://pages.di.unipi.it/brogi)
