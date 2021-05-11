const $ = require('jquery');
const Leaflet = require('./leaflet.ts');
const LeafletUtils = require('./leafletutils.ts');
const LeafletConfig = require('./leafletconfig.ts');
const Backbone = require('./backbone.js');
const latlongutils = require('./latlongutils.js');
const UploadPlanToMappingsTree = require('./uploadplantomappingstree.ts');
const WbPlanViewTreeHelper = require('./wbplanviewtreehelper.ts');
const WbPlanViewHelper = require('./wbplanviewhelper.ts');
const WbPlanViewModel = require('./wbplanviewmodel.ts').default;
const WbPlanViewModelHelper = require('./wbplanviewmodelhelper.ts');

module.exports = Backbone.View.extend({
  __name__: 'WbUtils',
  className: 'wbs-utils',
  events: {
    'click .wb-cell-navigation': 'navigateCells',
    'click .wb-navigation-text': 'toggleCellTypes',
    'click .wb-search-button': 'searchCells',
    'click .wb-replace-button': 'replaceCells',
    'click .wb-show-toolkit': 'toggleToolkit',
    'click .wb-geolocate': 'showGeoLocate',
    'click .wb-leafletmap': 'showLeafletMap',
    'click .wb-convert-coordinates': 'showCoordinateConversion',
  },
  initialize({ wbview }) {
    this.wbview = wbview;

    this.localityColumns = [];
    this.cellInfo = [];
    this.searchQuery = null;
  },
  render() {
    return this;
  },
  initCellInfo(row, col) {
    const cols = this.wbview.dataset.columns.length;
    if (typeof this.cellInfo[row * cols + col] === 'undefined') {
      this.cellInfo[row * cols + col] = {
        isNew: false,
        issues: [],
        matchesSearch: false,
      };
    }
  },
  navigateCells(e, matchCurrentCell = false) {
    const button = e.target;
    const direction = button.getAttribute('data-navigation-direction');
    const buttonParent = button.parentElement;
    const type = buttonParent.getAttribute('data-navigation-type');

    const numberOfColumns = this.wbview.dataset.columns.length;

    const selectedCell = this.wbview.hot.getSelectedLast();

    let currentPosition = 0;
    if (typeof selectedCell !== 'undefined') {
      const [row, col] = selectedCell;
      currentPosition = row * numberOfColumns + col;
    }

    const cellIsType = (info) => {
      if (typeof info !== 'object') return false;
      switch (type) {
        case 'invalidCells':
          return info.issues.length > 0;
        case 'newCells':
          return info.isNew;
        case 'searchResults':
          return info.matchesSearch;
        default:
          return false;
      }
    };

    let newPosition = currentPosition;
    let found = false;

    const overBound = currentPosition > this.cellInfo.length;
    const underBound = currentPosition < this.cellInfo.findIndex((el) => el);
    if (overBound || underBound) {
      newPosition = (overBound
        ? [...this.cellInfo].reverse()
        : this.cellInfo
      ).findIndex((cellInfo) => cellIsType(cellInfo));
      found = newPosition !== -1;
      if (found && overBound)
        newPosition = this.cellInfo.length - 1 - newPosition;
    }

    const cellInfoSubset =
      direction === 'next'
        ? this.cellInfo.slice(currentPosition + !matchCurrentCell)
        : this.cellInfo.slice(0, currentPosition - matchCurrentCell);

    if (!found) {
      newPosition = (direction === 'next'
        ? cellInfoSubset
        : cellInfoSubset.reverse()
      ).findIndex((cellInfo) => cellIsType(cellInfo));

      if (newPosition !== -1) {
        found = true;
        newPosition =
          direction === 'next'
            ? newPosition + currentPosition + !matchCurrentCell
            : currentPosition - matchCurrentCell - 1 - newPosition;
      }
    }

    if (found) {
      const row = Math.floor(newPosition / numberOfColumns);
      const col = newPosition - row * numberOfColumns;
      this.wbview.hot.selectCell(row, col, row, col);

      const cellRelativePosition = this.cellInfo.reduce(
        (count, info, i) =>
          count + (cellIsType(info) && i <= newPosition ? 1 : 0),
        0
      );
      const currentPositionElement = buttonParent.getElementsByClassName(
        'wb-navigation-position'
      )[0];
      currentPositionElement.innerText = cellRelativePosition;
    }

    return found;
  },
  toggleCellTypes(e) {
    const button = e.target;
    const buttonContainer = button.closest('.wb-navigation-section');
    const buttonLabel = buttonContainer.getAttribute('data-navigation-type');
    const cssClassName = `wb-hide-${WbPlanViewHelper.camelToKebab(
      buttonLabel
    )}`;
    this.el.classList.toggle(cssClassName);
  },
  searchCells(e) {
    const cols = this.wbview.dataset.columns.length;
    const button = e.target;
    const buttonContainer = button.parentElement;
    const navigationContainer = this.el.getElementsByClassName(
      'wb-navigation'
    )[0];
    const navigationPositionElement = navigationContainer.getElementsByClassName(
      'wb-navigation-position'
    )[0];
    const navigationTotalElement = navigationContainer.getElementsByClassName(
      'wb-navigation-total'
    )[0];
    const searchQueryElement = buttonContainer.getElementsByClassName(
      'wb-search-query'
    )[0];
    const navigationButton = navigationContainer.getElementsByClassName(
      'wb-cell-navigation'
    );
    const searchQuery = searchQueryElement.value;

    const searchPlugin = this.wbview.hot.getPlugin('search');
    const results = searchPlugin.query(searchQuery);
    this.searchQuery = searchQuery;

    this.cellInfo.forEach((cellInfo) => {
      cellInfo.matchesSearch = false;
    });
    results.forEach(({ row, col }) => {
      this.initCellInfo(row, col);
      this.cellInfo[row * cols + col].matchesSearch = true;
    });
    this.wbview.hot.render();

    navigationTotalElement.innerText = results.length;
    navigationPositionElement.innerText = 0;

    if (!this.navigateCells({ target: navigationButton[1] }, false))
      this.navigateCells({ target: navigationButton[0] }, true);
  },
  replaceCells(e) {
    const cols = this.wbview.dataset.columns.length;
    const button = e.target;
    const buttonContainer = button.parentElement;
    const replacementValueElement = buttonContainer.getElementsByClassName(
      'wb-replace-value'
    )[0];
    const replacementValue = replacementValueElement.value;

    const cellUpdates = [];
    this.cellInfo.forEach((info, i) => {
      if (info.matchesSearch) {
        const row = Math.floor(i / cols);
        const col = i - row * cols;
        const cellValue = this.wbview.hot.getDataAtCell(row, col);
        cellUpdates.push([
          row,
          col,
          cellValue.split(this.searchQuery).join(replacementValue),
        ]);
      }
    });

    this.wbview.hot.setDataAtCell(cellUpdates);
  },
  toggleToolkit() {
    const toolkit = this.el.getElementsByClassName('wb-toolkit')[0];
    if (toolkit.style.display === 'none') toolkit.style.display = '';
    else toolkit.style.display = 'none';
    this.wbview.resize.bind(this.wbview)();
  },
  fillCells({ startRow, endRow, col, value }) {
    this.wbview.hot.setDataAtCell(
      [...Array(endRow - startRow).keys()].map((index) => [
        startRow + index + 1,
        col,
        value,
      ])
    );
  },
  fillDown(props) {
    this.fillCells({
      ...props,
      value: this.wbview.hot.getDataAtCell(props.startRow, props.col),
    });
  },
  fillUp(props) {
    this.fillCells({
      ...props,
      startRow: props.startRow - 1,
      value: this.wbview.hot.getDataAtCell(props.endRow, props.col),
    });
  },
  fillCellsContextMenuItem(name, handlerFunction) {
    return {
      name: name,
      disabled: () =>
        this.wbview.hot
          .getSelected()
          ?.every((selection) => selection[0] === selection[2]) ?? false,
      callback: (_, selections) =>
        selections.forEach((selection) =>
          [
            ...Array(selection.end.col + 1 - selection.start.col).keys(),
          ].forEach((index) =>
            handlerFunction.bind(this)({
              startRow: selection.start.row,
              endRow: selection.end.row,
              col: selection.start.col + index,
            })
          )
        ) || this.wbview.hot.deselectCell(),
    };
  },
  findLocalityColumns() {
    if (this.wbview.dataset.uploadplan === null) return;

    const { mappingsTree } = UploadPlanToMappingsTree.uploadPlanToMappingsTree(
      this.wbview.dataset.columns,
      this.wbview.dataset.uploadplan
    );

    const arrayOfMappings = WbPlanViewTreeHelper.mappingsTreeToArrayOfSplitMappings(
      mappingsTree
    );

    const filteredArrayOfMappings = arrayOfMappings.reduce(
      (result, splitMappingPath) => {
        if (
          LeafletConfig.localityColumnsToSearchFor.indexOf(
            splitMappingPath.mappingPath[
              splitMappingPath.mappingPath.length - 1
            ]
          ) !== -1
        )
          result.push(splitMappingPath);

        return result;
      },
      []
    );

    const localityObjects = {};

    for (const { mappingPath, headerName } of filteredArrayOfMappings) {
      const [baseMappingPath, columnName] = [
        mappingPath.slice(0, -1),
        mappingPath.slice(-1),
      ];
      const baseMappingsPathString = baseMappingPath.join(
        WbPlanViewModel.pathJoinSymbol
      );

      localityObjects[baseMappingsPathString] ??= {};

      localityObjects[baseMappingsPathString][columnName] = headerName;
    }

    //finding geography tree mappings
    const geographyMappingPathsToSearchFor = [];
    const geographyRanksToSearchFor = ['country', 'state', 'county'];
    Object.keys(localityObjects).map((baseMappingsPathString) => {
      const baseMappingPath =
        baseMappingsPathString === ''
          ? []
          : baseMappingsPathString.split(WbPlanViewModel.pathJoinSymbol);

      const possibleGeographyMappingPath = [...baseMappingPath, 'geography'];

      geographyRanksToSearchFor.map((rankName) => {
        geographyMappingPathsToSearchFor.push([
          baseMappingsPathString,
          rankName,
          [
            ...possibleGeographyMappingPath,
            WbPlanViewModelHelper.formatTreeRank(rankName),
            'name',
          ].join(WbPlanViewModel.pathJoinSymbol),
        ]);
      });
    });

    arrayOfMappings.map(({ mappingPath, headerName }) =>
      geographyMappingPathsToSearchFor.some(
        ([baseMappingsPathString, rankName, targetMappingPath]) => {
          if (
            mappingPath.join(WbPlanViewModel.pathJoinSymbol) ===
            targetMappingPath
          ) {
            localityObjects[baseMappingsPathString][rankName] = headerName;
            return true;
          }
        }
      )
    );

    this.localityColumns = Object.values(localityObjects)
      .map((localityMapping) =>
        Object.fromEntries(
          Object.entries(localityMapping).map(([columnName, headerName]) => [
            columnName,
            this.wbview.dataset.columns.indexOf(headerName),
          ])
        )
      )
      .filter((localityColumns) =>
        LeafletConfig.requiredLocalityColumns.every(
          (requiredColumnName) => requiredColumnName in localityColumns
        )
      );

    [
      ...new Set([
        ...(this.localityColumns.length !== 0 && !this.wbview.uploaded
          ? ['wb-geolocate', 'wb-leafletmap', 'wb-convert-coordinates']
          : []),
        ...(this.localityColumns.length === 0 ? [] : ['wb-leafletmap']),
      ]),
    ].map(
      (className) =>
        this.el.getElementsByClassName(className)[0] &&
        (this.el.getElementsByClassName(className)[0].style.display = null)
    );
  },
  getGeoLocateQueryURL(
    currentLocalityColumns,
    selectedRow,
    getDataAtCell,
    getDataAtRow
  ) {
    if (currentLocalityColumns === false) return;

    let queryString;

    if (
      typeof currentLocalityColumns.country !== 'undefined' &&
      typeof currentLocalityColumns.state !== 'undefined'
    ) {
      const data = Object.fromEntries(
        ['country', 'state', 'county', 'localityname'].map((columnName) => [
          columnName,
          typeof currentLocalityColumns[columnName] === 'undefined'
            ? undefined
            : encodeURIComponent(
                getDataAtCell(selectedRow, currentLocalityColumns[columnName])
              ),
        ])
      );

      queryString = `country=${data.country}&state=${data.state}`;

      if (typeof data.county !== 'undefined')
        queryString += `&county=${data.county}`;

      if (typeof data.localityname !== 'undefined')
        queryString += `&locality=${data.localityname}`;
    } else {
      const pointDataDict = LeafletUtils.getLocalityCoordinate(
        getDataAtRow(selectedRow),
        currentLocalityColumns
      );

      if (!pointDataDict) return;

      const { latitude1, longitude1, localityname = '' } = pointDataDict;

      const pointDataList = [latitude1, longitude1];

      if (localityname !== '') pointDataList.push(localityname);

      queryString = `points=${pointDataList.join('|')}`;
    }

    return `https://www.geo-locate.org/web/WebGeoreflight.aspx?v=1&w=900&h=400&${queryString}`;
  },
  showGeoLocate() {
    // don't allow opening more than one window)
    if ($('#geolocate-window').length !== 0) return;

    let $this = this;

    const selectedRegions = this.wbview.hot.getSelected() || [[0, 0, 0, 0]];
    const selections = selectedRegions.map(([startRow, column, endRow]) =>
      startRow < endRow
        ? [startRow, endRow, column]
        : [endRow, startRow, column]
    );
    const selectedCells = selections.flatMap(([startRow, endRow, column]) =>
      [...Array(endRow - startRow + 1)].map((_, index) =>
        [startRow + index, column].join(WbPlanViewModel.pathJoinSymbol)
      )
    );
    const uniqueSelectedCells = [...new Set(selectedCells)];
    const finalSelectedCells = uniqueSelectedCells.map((selectedCell) =>
      selectedCell
        .split(WbPlanViewModel.pathJoinSymbol)
        .map((index) => parseInt(index))
    );

    if (finalSelectedCells.length === 0) return;

    let currentCellIndex = 0;
    let geolocateQueryUrl = false;
    let currentLocalityColumns = [];

    function updateGeolocateUrl() {
      currentLocalityColumns = LeafletUtils.getLocalityColumnsFromSelectedCell(
        $this.localityColumns,
        finalSelectedCells[currentCellIndex][1]
      );

      geolocateQueryUrl = $this.getGeoLocateQueryURL(
        currentLocalityColumns,
        finalSelectedCells[currentCellIndex][0],
        $this.wbview.hot.getDataAtCell.bind($this.wbview.hot),
        $this.wbview.hot.getDataAtRow.bind($this.wbview.hot)
      );
    }

    updateGeolocateUrl();

    if (geolocateQueryUrl === false) return;

    const handleAfterDialogClose = () =>
      window.removeEventListener('message', handleGeolocateResult, false);

    const dialog = $(`<div />`, { id: 'geolocate-window' }).dialog({
      width: 960,
      height: finalSelectedCells.length === 1 ? 680 : 740,
      title: 'GEOLocate',
      close: function () {
        $(this).remove();
        handleAfterDialogClose();
      },
    });

    const updateGeolocate = () =>
      dialog.html(`<iframe
        style="
            width: 100%;
            height: 100%;
            border: none;"
        src="${geolocateQueryUrl}"></iframe>`);
    updateGeolocate();

    const updateSelectedRow = () =>
      $this.wbview.hot.selectRows(finalSelectedCells[currentCellIndex][0]);
    updateSelectedRow();

    function changeSelectedCell(newSelectedCell) {
      currentCellIndex = newSelectedCell;

      updateGeolocateUrl();

      if (geolocateQueryUrl === false) return;

      updateGeolocate();

      updateSelectedRow();

      updateButtons();
    }

    const updateButtons = () =>
      dialog.dialog(
        'option',
        'buttons',
        finalSelectedCells.length > 1
          ? [
              {
                text: 'Previous',
                click: () => changeSelectedCell(currentCellIndex - 1),
                disabled: currentCellIndex === 0,
              },
              {
                text: 'Next',
                click: () => changeSelectedCell(currentCellIndex + 1),
                disabled: finalSelectedCells.length <= currentCellIndex + 1,
              },
            ]
          : []
      );
    updateButtons();

    const handleGeolocateResult = (event) => {
      const dataColumns = event.data.split('|');
      if (dataColumns.length !== 4 || event.data === '|||') return;

      $this.wbview.hot.setDataAtCell(
        ['latitude1', 'longitude1', 'latlongaccuracy']
          .map((column, index) => {
            if (typeof currentLocalityColumns[column] !== 'undefined')
              return [
                finalSelectedCells[currentCellIndex][0],
                currentLocalityColumns[column],
                dataColumns[index],
              ];
          })
          .filter((record) => typeof record !== 'undefined')
      );

      if (finalSelectedCells.length === 1) {
        dialog.dialog('close');
        handleAfterDialogClose();
      }
    };

    window.addEventListener('message', handleGeolocateResult, false);
  },
  showLeafletMap() {
    if ($('#leaflet-map').length !== 0) return;

    const localityPoints = LeafletUtils.getLocalitiesDataFromSpreadsheet(
      this.localityColumns,
      this.wbview.dataset.rows
    );

    Leaflet.showLeafletMap({
      localityPoints,
      markerClickCallback: (localityPoint) => {
        const rowNumber = localityPoints[localityPoint].rowNumber;
        const selectedColumn =
          typeof this.wbview.hot.getSelectedLast() === 'undefined'
            ? 0
            : this.wbview.hot.getSelectedLast()[1];
        // select the first cell to scroll the view
        this.wbview.hot.selectCell(rowNumber, selectedColumn);
        this.wbview.hot.selectRows(rowNumber); // select an entire row
      },
    });
  },
  showCoordinateConversion() {
    if ($('.latlongformatoptions').length !== 0) return;

    const columnHandlers = {
      latitude1: 'Lat',
      longitude1: 'Long',
      latitude2: 'Lat',
      longitude2: 'Long',
    };

    const columnsToSearchFor = Object.keys(columnHandlers);

    const coordinateColumns = this.localityColumns.reduce(
      (coordinateColumns, columnIndexes) => [
        ...coordinateColumns,
        ...Object.entries(columnIndexes).filter(
          ([columnName]) => columnsToSearchFor.indexOf(columnName) !== -1
        ),
      ],
      []
    );

    if (coordinateColumns.length === 0) return;

    const options = [
      {
        optionName: 'DD.DDDD (32.7619)',
        conversionFunctionName: 'toDegs',
        showCardinalDirection: false,
      },
      {
        optionName: 'DD MMMM (32. 45.714)',
        conversionFunctionName: 'toDegsMins',
        showCardinalDirection: false,
      },
      {
        optionName: 'DD MM SS.SS (32 45 42.84)',
        conversionFunctionName: 'toDegsMinsSecs',
        showCardinalDirection: false,
      },
      {
        optionName: 'DD.DDDD N/S/E/W (32.7619 N)',
        conversionFunctionName: 'toDegs',
        showCardinalDirection: true,
      },
      {
        optionName: 'DD MM.MM N/S/E/W (32 45.714 N)',
        conversionFunctionName: 'toDegsMins',
        showCardinalDirection: true,
      },
      {
        optionName: 'DD MM SS.SS N/S/E/W (32 45 42.84 N)',
        conversionFunctionName: 'toDegsMinsSecs',
        showCardinalDirection: true,
      },
    ];

    const closeDialog = () => {
      dialog.off('change', handleOptionChange);
      dialog.remove();
    };

    const dialog = $(
      `<ul class="latlongformatoptions">
        ${Object.values(options)
          .map(
            ({ optionName }, optionIndex) =>
              `<li>
            <label>
              <input
                type="radio"
                name="latlongformat"
                value="${optionIndex}"
              >
              ${optionName}
            </label>
          </li>`
          )
          .join('')}
        <li>
          <br>
          <label>
            <input type="checkbox" name="includesymbols">
            Include Symbols
          </label>
        </li>
      </ul>`
    ).dialog({
      title: 'Coordinate format converter',
      close: closeDialog,
      buttons: [{ text: 'Close', click: closeDialog }],
    });

    const handleOptionChange = () => {
      const includeSymbolsCheckbox = dialog.find(
        'input[name="includesymbols"]'
      );
      const includeSymbols = includeSymbolsCheckbox.is(':checked');

      const selectedOption = dialog.find('input[type="radio"]:checked');
      if (selectedOption.length === 0) return;

      const optionValue = selectedOption.attr('value');
      if (typeof options[optionValue] === 'undefined') return;

      const { conversionFunctionName, showCardinalDirection } = options[
        optionValue
      ];
      const includeSymbolsFunction = includeSymbols
        ? (coordinate) => coordinate
        : (coordinate) => coordinate.replace(/[^\w\s\-.]/gm, '');
      const lastChar = (value) => value[value.length - 1];
      const removeLastChar = (value) => value.slice(0, -1);
      const endsWith = (value, charset) =>
        charset.indexOf(lastChar(value)) !== -1;
      const stripCardinalDirections = (finalValue) =>
        showCardinalDirection
          ? finalValue
          : endsWith(finalValue, 'SW')
          ? '-' + removeLastChar(finalValue)
          : endsWith(finalValue, 'NE')
          ? removeLastChar(finalValue)
          : finalValue;

      this.wbview.hot.setDataAtCell(
        coordinateColumns
          .map(([columnName, columnIndex]) =>
            this.wbview.hot
              .getDataAtCol(columnIndex)
              .map((cellValue, rowIndex) => [
                latlongutils[columnHandlers[columnName]].parse(cellValue),
                rowIndex,
              ])
              .filter(([coordinate]) => coordinate !== null)
              .map(([coordinate, rowIndex]) => [
                rowIndex,
                columnIndex,
                includeSymbolsFunction(
                  stripCardinalDirections(
                    coordinate[conversionFunctionName]().format()
                  )
                ).trim(),
              ])
          )
          .flat()
      );
    };
    dialog.on('change', handleOptionChange);
  },
});
