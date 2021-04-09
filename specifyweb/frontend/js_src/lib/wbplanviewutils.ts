import $ from 'jquery';
import automapper from './automapper';
import {
  PublicWBPlanViewProps,
  WBPlanViewWrapperProps,
} from './components/wbplanview';
import {
  AutomapperSuggestion,
  FullMappingPath,
  MappingLine,
  MappingPath,
  SelectElementPosition,
} from './components/wbplanviewmapper';
import {
  LoadingState,
  MappingState,
} from './components/wbplanviewstatereducer';
import { mappingsTreeToUploadPlan } from './mappingstreetouploadplan';
import navigation from './navigation';
import { findDuplicateMappings } from './wbplanviewhelper';
import dataModelStorage from './wbplanviewmodel';
import {
  formatReferenceItem,
  getMaxToManyValue,
  showRequiredMissingFields,
  valueIsReferenceItem,
  valueIsTreeRank,
} from './wbplanviewmodelhelper';
import { getMappingLineData } from './wbplanviewnavigator';
import { ChangeSelectElementValueAction } from './wbplanviewreducer';
import {
  arrayOfMappingsToMappingsTree,
  MappingsTree,
  traverseTree,
} from './wbplanviewtreehelper';


export const goBack = (props: PublicWBPlanViewProps): void =>
  navigation.go(`/workbench/${props.dataset.id}/`);

export function savePlan(
  props: WBPlanViewWrapperProps,
  state: MappingState,
  ignoreValidation = false,
): LoadingState | MappingState {
  const validationResultsState = validate(state);
  if (
    !ignoreValidation &&
    validationResultsState.validationResults.length !== 0
  )
    return validationResultsState;

  // props.wb.set('ownerPermissionLevel', props.mappingIsTemplated ? 1 : 0);
  const uploadPlan = mappingsTreeToUploadPlan(
    state.baseTableName,
    getMappingsTree(state.lines, true),
    state.mustMatchPreferences,
  );

  void (
    $.ajax(`/api/workbench/dataset/${props.dataset.id}/`, {
      type: 'PUT',
      data: JSON.stringify({
        'uploadplan':
        uploadPlan,
      }),
      dataType: 'json',
      processData: false,
    }).done(() => {

      if (state.changesMade)
        props.removeUnloadProtect();

      goBack(props);

    })
  );

  return state;
}

/* Validates the current mapping and shows error messages if needed */
export function validate(state: MappingState): MappingState {

  const validationResults = showRequiredMissingFields(
    state.baseTableName,
    getMappingsTree(state.lines, true),
  );

  return {
    ...state,
    type: 'MappingState',
    // Show mapping view panel if there were validation errors
    showMappingView:
      state.showMappingView ||
      Object.values(validationResults).length !== 0,
    mappingsAreValidated: Object.values(validationResults).length === 0,
    validationResults,
  };
}


/* Unmap headers that have a duplicate mapping path */
export function deduplicateMappings(
  lines: MappingLine[],
  focusedLine: number | false,
): MappingLine[] {

  const arrayOfMappings = getArrayOfMappings(lines);
  const duplicateMappingIndexes = findDuplicateMappings(
    arrayOfMappings,
    focusedLine,
  );

  return lines.map((line, index) =>
    duplicateMappingIndexes.indexOf(index) === -1 ?
      line :
      {
        ...line,
        mappingPath: line.mappingPath.slice(0, -1),
      },
  );

}


export function getArrayOfMappings(
  lines: MappingLine[],
  includeHeaders: true,
): FullMappingPath[];
export function getArrayOfMappings(
  lines: MappingLine[],
  includeHeaders?: false,
): MappingPath[];
export function getArrayOfMappings(
  lines: MappingLine[],
  includeHeaders = false,
): (MappingPath | FullMappingPath)[] {
  return lines.filter(({mappingPath: mappingPath}) =>
    mappingPathIsComplete(mappingPath),
  ).map(({mappingPath, type, name, options}) =>
    includeHeaders ?
      [...mappingPath, type, name, options] :
      mappingPath,
  );
}

export const getMappingsTree = (
  lines: MappingLine[],
  includeHeaders = false,
): MappingsTree =>
  arrayOfMappingsToMappingsTree(
    // overloading does not seem to work nicely with dynamic types
    includeHeaders ?
      getArrayOfMappings(lines, true) :
      getArrayOfMappings(lines, false),
    includeHeaders,
  );

/* Get a mappings tree branch given a particular starting mapping path */
export function getMappedFields(
  lines: MappingLine[],
  // a mapping path that would be used as a filter
  mappingPathFilter: MappingPath,
): MappingsTree {
  const mappingsTree = traverseTree(getMappingsTree(lines), mappingPathFilter);
  return typeof mappingsTree === 'object' ?
    mappingsTree :
    {};
}

export const pathIsMapped = (
  lines: MappingLine[],
  mappingPath: MappingPath,
): boolean =>
  Object.keys(
    getMappedFields(lines, mappingPath.slice(0, -1)),
  ).indexOf(mappingPath.slice(-1)[0]) !== -1;


export const mappingPathIsComplete = (mappingPath: MappingPath): boolean =>
  mappingPath[mappingPath.length - 1] !== '0';


/*
* The most important function in `wbplanview`
* It decides how to modify the mapping path when a different picklist
* item is selected.
* It is also responsible for deciding when to spawn a new box to the right
* of the current one
* */
export function mutateMappingPath({
  lines,
  mappingView,
  line,
  index,
  value,
  currentTableName,
  newTableName,
}: Omit<ChangeSelectElementValueAction, 'type'> & {
  readonly lines: MappingLine[],
  readonly mappingView: MappingPath,
  readonly isRelationship: boolean,
  readonly currentTableName: string,
  readonly newTableName: string,
}): MappingPath {

  // get mapping path from selected line or mapping view
  let mappingPath = [...(
    line === 'mappingView' ?
      mappingView :
      lines[line].mappingPath
  )];

  // get relationship type from current picklist to the next one both for
  // current value and next value
  const currentRelationshipType =
    dataModelStorage.tables[currentTableName]?.fields[
      mappingPath[index+1] || ''
    ]?.type || '';
  const newRelationshipType =
    dataModelStorage.tables[newTableName]?.fields[value]?.type || '';

  // don't reset the boxes to the right of the current box if relationship
  // type is the same (or non existent in both cases) and the new box is a
  // -to-many index, a tree rank or a different relationship to the same table
  const preserveMappingPathToRight =
    currentRelationshipType === newRelationshipType && (
      valueIsReferenceItem(value) ||
      valueIsTreeRank(value) ||
      currentTableName === newTableName
    );

  // when `Add` is selected in the list of -to-many indexes, replace it by
  // creating a new -to-many index
  if (value === 'add') {
    const mappedFields = Object.keys(
      getMappedFields(lines, mappingPath.slice(0, index)),
    );
    const maxToManyValue = getMaxToManyValue(mappedFields);
    mappingPath[index] = formatReferenceItem(maxToManyValue + 1);
  }
  else if (preserveMappingPathToRight)
    mappingPath[index] = value;
  else  // clear mapping path to the right of current box
    mappingPath = [...mappingPath.slice(0, index), value];

  return mappingPath;

}


// the maximum count of suggestions to show in the suggestions box
const MAX_SUGGESTIONS_COUNT = 3;

/*
* Show automapper suggestion on top of an opened `CLOSED_LIST`
* The automapper suggestions are shown only if the current box doesn't have
* a value selected
* */
export async function getAutomapperSuggestions({
  lines,
  line,
  index,
  baseTableName,
}: SelectElementPosition & {
  readonly lines: MappingLine[],
  readonly baseTableName: string,
}): Promise<AutomapperSuggestion[]> {
  const localMappingPath = [...lines[line].mappingPath];

  if (  // don't show suggestions
    (  // if opened picklist has a value selected
      localMappingPath.length - 1 !== index ||
      mappingPathIsComplete(localMappingPath)
    ) ||  // or if header is a new column / new static column
    lines[line].type !== 'existingHeader'
  )
    return [];

  const mappingLineData = getMappingLineData({
    baseTableName,
    mappingPath: mappingPathIsComplete(localMappingPath) ?
      localMappingPath :
      localMappingPath.slice(0, localMappingPath.length - 1),
    iterate: false,
    customSelectType: 'SUGGESTION_LIST',
    getMappedFields: getMappedFields.bind(null, lines),
  });

  // don't show suggestions if picklist has only one field / no fields
  if (
    mappingLineData.length === 1 &&
    Object.keys(mappingLineData[0].fieldsData).length < 2
  )
    return [];

  const baseMappingPath = localMappingPath.slice(0, -1);

  let pathOffset = 0;
  if (
    mappingLineData.length === 1 &&
    mappingLineData[0].customSelectSubtype === 'toMany'
  ) {
    baseMappingPath.push('#1');
    pathOffset = 1;
  }

  const allAutomapperResults = Object.entries((
    new automapper({
      headers: [lines[line].name],
      baseTable: baseTableName,
      startingTable: mappingLineData.length === 0 ?
        baseTableName :
        mappingLineData[mappingLineData.length - 1].tableName,
      path: baseMappingPath,
      pathOffset,
      allowMultipleMappings: true,
      checkForExistingMappings: true,
      scope: 'suggestion',
      pathIsMapped: pathIsMapped.bind(null, lines),
    })
  ).map({
    commitToCache: false,
  }));

  if (allAutomapperResults.length === 0)
    return [];

  let automapperResults = allAutomapperResults[0][1];

  if (automapperResults.length > MAX_SUGGESTIONS_COUNT)
    automapperResults = automapperResults.slice(0, 3);

  return automapperResults.map(automapperResult => (
    {
      mappingPath: automapperResult,
      mappingLineData: getMappingLineData({
        baseTableName,
        mappingPath: automapperResult,
        customSelectType: 'SUGGESTION_LINE_LIST',
        getMappedFields: getMappedFields.bind(null, lines),
      }).slice(baseMappingPath.length - pathOffset),
    }
  ));
}