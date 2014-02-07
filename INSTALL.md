Thanks for downloading pfam_maps.

To work with pfam_maps, you need a postgres instance of the ChEMBL database, which can be obtained [here](ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/). You also need django, configured to connect to your ChEMBL instance. The pfam_maps app operates on an additional table that can be added to the database using the [pfam_maps_loader](https://github.com/fak/pfam_map_loader/) repo.

You can activate he pfam_mpas app by add it to the INSTALLED_APPS section in your setting file and copying the repo-folder into your django project folder. You should then be able to run the app on the django dev-server. 
