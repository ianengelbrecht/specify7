"use strict";

const $ = require('jquery');
const latlongutils = require('./latlongutils.js');

const L = require('leaflet');
require('leaflet/dist/leaflet.css');
/* This code is needed to properly load the images in the Leaflet CSS */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

//create a "full screen" button
L.Control.FullScreen = L.Control.extend({
    onAdd: map => {
        const img = L.DomUtil.create('img');
        img.style.cursor = 'pointer';

        L.DomEvent
            .on(img, 'click', L.DomEvent.stopPropagation)
            .on(img, 'click', L.DomEvent.preventDefault)
            .on(img, 'click', ()=>toggleFullScreen(map));

        img.src = '/static/img/full_screen.png';
        img.style.width = '50px';

        this.img = img;

        return img;
    },

    onRemove: map => {
        L.DomEvent
            .off(this.img, 'click', L.DomEvent.stopPropagation)
            .off(this.img, 'click', L.DomEvent.preventDefault)
            .off(this.img, 'click', ()=>toggleFullScreen(map));
    }
});

function toggleFullScreen(map){
    const dialog = $(map._container.closest('.ui-dialog-content'));
    const [width, height] = dialog[0].parentElement.style.top === '0px' ?
        [900, 600] :
        [window.innerWidth, window.innerHeight];
    dialog.dialog('option','width', width);
    dialog.dialog('option','height', height);
    map.invalidateSize();
}


const Leaflet = {

    cellIsValid: (row, column_indexes, column_name) =>
        typeof column_indexes[column_name] !== "undefined" &&
        column_indexes[column_name] !== -1 &&
        row[column_indexes[column_name]] !== null,

    formatCoordinate(row, column_indexes, column_name){
        if (row[column_indexes[column_name]] === 0 || row[column_indexes[column_name]] === '0')
            return 0;
        const coordinate = latlongutils.parse(row[column_indexes[column_name]]).toDegs();
        return coordinate._components[0] * coordinate._sign;
    },

    getLocalityCoordinate(row, column_indexes, accept_polygons = false){

        const cellIsValid = (column_name) => this.cellIsValid(row, column_indexes, column_name);
        const formatCoordinate = (column_name) => this.formatCoordinate(row, column_indexes, column_name);

        if (
            !cellIsValid('latitude1') ||
            !cellIsValid('longitude1')
        )
            return false;

        const point_data = {};
        try {

            point_data.latitude1 = formatCoordinate('latitude1');
            point_data.longitude1 = formatCoordinate('longitude1');

            if (
                accept_polygons &&
                cellIsValid('latitude2') &&
                cellIsValid('longitude2') &&
                (
                    !cellIsValid('latlongtype') ||
                    row[column_indexes.latlongtype].toLowerCase() !== 'point'
                )
            ) {
                point_data.latitude2 = formatCoordinate('latitude2');
                point_data.longitude2 = formatCoordinate('longitude2');
                point_data.latlongtype = (
                    cellIsValid('latlongtype') &&
                    row[column_indexes.latlongtype].toLowerCase() === 'line'
                ) ? 'Line' : 'Rectangle';
            }
        } catch (e) {
            return false;
        }

        if (cellIsValid('localityname'))
            point_data.localityname = row[column_indexes.localityname];

        if (cellIsValid('latlongaccuracy'))
            point_data.latlongaccuracy = row[column_indexes.latlongaccuracy];

        return point_data;

    },

    getLocalityColumnsFromSelectedCell(locality_columns, selected_column){

        if (locality_columns.length === 0)
            return false;


        if (locality_columns.length > 1) {
            // if there are multiple localities present in a row, check which group this field belongs too
            let current_locality_columns;
            const locality_columns_to_search_for = ['localityname', 'latitude1', 'longitude1', 'latlongtype', 'latlongaccuracy'];
            if (locality_columns.some(local_locality_columns =>
                Object.fromEntries(local_locality_columns).some((field_name, column_index) => {
                    if (
                        locality_columns_to_search_for.indexOf(field_name) !== -1 &&
                        column_index === selected_column
                    )
                        return current_locality_columns = local_locality_columns;
                })
            ))
                return current_locality_columns;
            else
                return false;  // if can not determine the group the column belongs too
        }
        else
            return locality_columns[0];

    },

    getLocalitiesDataFromSpreadsheet(locality_columns, spreadsheet_data){

        return locality_columns.reduce((locality_points, column_indexes) => {

            spreadsheet_data.map((row, index) => {
                const locality_coordinate = this.getLocalityCoordinate(row, column_indexes, true);

                if (!locality_coordinate)
                    return;

                locality_coordinate.rowNumber = index;
                locality_points.push(locality_coordinate);
            });

            return locality_points;

        }, []);

    },

    getLocalityDataFromLocalityResource(locality_resource){
        return new Promise(resolve =>
            Promise.all(
                locality_fields_to_get.map(field_name =>
                    new Promise(resolve =>
                        locality_resource.rget(field_name).done(field_value =>
                            resolve([field_name, field_value])
                        )
                    )
                )
            ).then(locality_fields_array => {
                const locality_fields = Object.fromEntries(locality_fields_array);
                resolve(locality_fields);
            })
        );
    },

    getMarkersFromLocalityResource(locality_resource, icon_class){
        return new Promise(resolve =>
            this.getLocalityDataFromLocalityResource(locality_resource).then(locality_fields => {
                const markers = this.displayLocalityOnTheMap({
                    locality_data: locality_fields,
                    icon_class: icon_class
                });
                resolve(markers);
            }));
    },

    showLeafletMap({
        locality_points: localityPoints = [],
        marker_click_callback: markerClickCallback = () => {
        },
        leafletMap_container
    }){

        if (typeof leafletMap_container === "undefined")
            leafletMap_container = $(`<div></div>`);

        leafletMap_container.dialog({
            width: 900,
            height: 600,
            title: "Leaflet map",
            close: function(){
                map.remove();
                $(this).remove();
            },
        });


        let defaultCenter = [0, 0];
        let defaultZoom = 1;
        if (localityPoints.length > 0) {
            defaultCenter = [localityPoints[0].latitude1, localityPoints[0].longitude1];
            defaultZoom = 5;
        }

        const map = L.map(leafletMap_container[0], {
            layers: [
                Object.values(leaflet_tile_servers.base_maps)[0],
            ],
        }).setView(defaultCenter, defaultZoom);
        const control_layers = L.control.layers(leaflet_tile_servers.base_maps, leaflet_tile_servers.overlays);
        control_layers.addTo(map);

        let index = 0;
        Leaflet.addMarkersToMap(
            map,
            control_layers,
            localityPoints.map(point_data_dict =>
                this.displayLocalityOnTheMap({
                    locality_data: point_data_dict,
                    markerClickCallback: markerClickCallback.bind(
                        null,
                        index++
                    ),
                    map: map
                })
            ).flat(),
            'Polygon boundaries',
            true
        );

        //add button that toggles full-screen
        L.control.fullScreen = opts =>
            new L.Control.FullScreen(opts);
        L.control.fullScreen({ position: 'bottomleft' }).addTo(map);

        return map;

    },

    addMarkersToMap(map, control_layers, markers, layer_name, enable=false){

        if(markers.length === 0)
            return;

        const layer = L.layerGroup(markers);
        control_layers.addOverlay(layer, layer_name);
        layer.addTo(map);

        if(enable)
            map.addLayer(layer);

    },

    displayLocalityOnTheMap({
        locality_data: {
            latitude1,
            longitude1,
            latitude2 = null,
            longitude2 = null,
            latlongtype = null,
            latlongaccuracy = null,
            localityname = null,
        },
        marker_click_callback,
        map,
        icon_class
    }){

        const icon = new L.Icon.Default();
        if (typeof icon_class !== "undefined")
            icon.options.className = icon_class;

        const create_a_point = (latitude1, longitude1) =>
            L.marker([latitude1, longitude1], {
                icon: icon,
            });

        let vectors = [];

        if (latitude2 === null || longitude2 === null) {

            // a point
            if (latlongaccuracy === null || latlongaccuracy === "0")
                vectors.push(create_a_point(latitude1, longitude1));

            // a circle
            else
                vectors.push(
                    L.circle([latitude1, longitude1], {
                        icon: icon,
                        radius: latlongaccuracy
                    }),
                    create_a_point(latitude1, longitude1)
                );

        }

        else
            vectors.push(
                latlongtype === 'Line' ?
                    // a line
                    new L.Polyline([
                        [latitude1, longitude1],
                        [latitude2, longitude2]
                    ], {
                        icon: icon,
                        weight: 3,
                        opacity: 0.5,
                        smoothFactor: 1
                    }) :
                    // a polygon
                    L.polygon([
                        [latitude1, longitude1],
                        [latitude2, longitude1],
                        [latitude2, longitude2],
                        [latitude1, longitude2]
                    ], {
                        icon: icon,
                    }),
                create_a_point(latitude1, longitude1),
                create_a_point(latitude2, longitude2)
            );


        const polygon_boundaries = [];

        let is_first_vector = true;
        vectors.map(vector => {

            if (is_first_vector && typeof map !== "undefined") {
                vector.addTo(map);
                is_first_vector = false;
            }
            else
                polygon_boundaries.push(vector);

            if (typeof marker_click_callback === "string")
                vector.bindPopup(marker_click_callback);
            else if (typeof marker_click_callback === "function")
                vector.on('click', marker_click_callback);
            else if (typeof marker_click_callback === "undefined" && localityname !== null)
                vector.bindPopup(localityname);

        });

        return polygon_boundaries;

    },

    showCOMap(list_of_layers_raw){

        const list_of_layers = [
            ...co_map_tile_servers.map(({transparent, layer_label})=>
                ({
                    transparent: transparent,
                    layer_label: layer_label,
                    tile_layer: leaflet_tile_servers[(transparent?'overlays':'base_maps')][layer_label]
                })
            ),
            ...list_of_layers_raw.map(({transparent, layer_label, tile_layer: {map_url, options}}) =>
                ({
                    transparent: transparent,
                    layer_label: layer_label,
                    tile_layer: L.tileLayer.wms(map_url, options)
                })
            )
        ];

        const format_layers_dict = (list_of_layers) => Object.fromEntries(
            list_of_layers.map(({_, layer_label, tile_layer}) =>
                [layer_label, tile_layer]
            )
        );

        const all_layers = Object.values(format_layers_dict(list_of_layers));
        const overlay_layers = format_layers_dict(list_of_layers.filter(({transparent}) => transparent));

        const map = L.map('lifemapper_leaflet-map', {
            layers: all_layers,
        }).setView([0, 0], 1);

        const layer_group = L.control.layers({}, overlay_layers);
        layer_group.addTo(map);

        return [map, layer_group];

    },

};



const leaflet_tile_servers = {
    base_maps: {
        'OpenStreetMap Standart': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        'OpenStreetMap Humanitarian': L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            subdomains: ['a','b'],
        }),
        'OpenStreetMap CyclOSM': L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
          options: {
            maxZoom: 20,
            attribution: '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: {attribution.OpenStreetMap}'
          }
        }),
        'OpenStreetMap Transport': L.tileLayer('https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png', {
          options: {
            maxZoom: 20,
            attribution: '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: {attribution.OpenStreetMap}'
          }
        }),
        'ESRI: World_Street_Map': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Esri, HERE, Garmin, USGS, Intermap, INCREMENT P, NRCan, Esri Japan, METI, Esri China (Hong Kong), Esri Korea, Esri (Thailand), NGCC, (c) OpenStreetMap contributors, and the GIS User Community',
        }),
        'ESRI: World_Topo_Map': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Sources: Esri, HERE, Garmin, Intermap, increment P Corp., GEBCO, USGS, FAO, NPS, NRCAN, GeoBase, IGN, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), (c) OpenStreetMap contributors, and the GIS User Community',
        }),
        'ESRI: WorldImagery': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        }),
        'GeoportailFrance orthos': L.tileLayer('https://wxs.ign.fr/{apikey}/geoportail/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&STYLE={style}&TILEMATRIXSET=PM&FORMAT={format}&LAYER=ORTHOIMAGERY.ORTHOPHOTOS&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}', {
            attribution: '<a target="_blank" href="https://www.geoportail.gouv.fr/">Geoportail France</a>',
            bounds: [[-75, -180], [81, 180]],
            minZoom: 2,
            maxZoom: 19,
            apikey: 'choisirgeoportail',
            format: 'image/jpeg',
            style: 'normal'
        }),
        'USGS USImagery': L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 20,
            attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
        }),
        'NASAGIBS ModisTerraTrueColorCR': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_CorrectedReflectance_TrueColor/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 9,
          format: 'jpg',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
        'NASAGIBS ModisTerraBands367CR': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_CorrectedReflectance_TrueColor/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 9,
          format: 'jpg',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
        'NASAGIBS ViirsEarthAtNight2012': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 8,
          format: 'jpg',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
        'NASAGIBS ModisTerraLSTDay': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_Land_Surface_Temp_Day/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 7,
          opacity: 0.75,
          format: 'png',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
        'NASAGIBS ModisTerraAOD': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_Aerosol/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 6,
          opacity: 0.75,
          format: 'png',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
        'NASAGIBS ModisTerraChlorophyll': L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_Chlorophyll_A/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
          attribution:
            'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System ' +
            '(<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
          bounds: [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
          minZoom: 1,
          maxZoom: 7,
          opacity: 0.75,
          format: 'png',
          time: '',
          tilematrixset: 'GoogleMapsCompatible_Level'
        }),
    },
    overlays: {
        'ESRI: Reference/World_Boundaries_and_Places': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Esri, HERE, Garmin, (c) OpenStreetMap contributors, and the GIS user community',
        }),
        'ESRI: Reference/World_Boundaries_and_Places_Alternate': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places_Alternate/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Esri, HERE, Garmin, (c) OpenStreetMap contributors, and the GIS user community',
        }),
        'ESRI: Canvas/World_Dark_Gray_Reference': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Esri, HERE, Garmin, (c) OpenStreetMap contributors, and the GIS user community\n',
        }),
        'ESRI: Reference/World_Reference_Overlay': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Reference_Overlay/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Sources: Esri, Garmin, USGS, NPS',
        }),
    }
};

const co_map_tile_servers = [
    {
        transparent: false,
        layer_label: 'ESRI: WorldImagery',
    },
    {
        transparent: true,
        layer_label: 'ESRI: Canvas/World_Dark_Gray_Reference',
    }
];

const locality_fields_to_get = ['localityname', 'latitude1', 'longitude1', 'latitude2', 'longitude2', 'latlongtype', 'latlongaccuracy'];

module.exports = Leaflet;