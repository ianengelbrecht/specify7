/**
 * WB Upload results Typings
 *
 * @module
 */

import type { LocalizedString } from 'typesafe-i18n';
import type { State } from 'typesafe-reducer';

import { backEndText } from '../../localization/backEnd';
import type { IR, RA, RR } from '../../utils/types';
import { localized } from '../../utils/types';
import {
  formatConjunction,
  formatDisjunction,
} from '../Atoms/Internationalization';
import { getField } from '../DataModel/helpers';
import { tables } from '../DataModel/tables';
import type { Tables } from '../DataModel/types';

/*
 * If an UploadResult involves a tree record, this metadata indicates
 * where in the tree the record resides
 */
type TreeInfo = {
  // The tree rank a record relates to
  readonly rank: string;
  // The name of the tree node a record relates to
  readonly name: string;
};

/*
 * Records metadata about an UploadResult indicating the tables, data set
 * columns, and any tree information involved
 */
type ReportInfo = {
  // The name of the table a record relates to
  readonly tableName: keyof Tables;
  // The columns from the data set a record relates to
  readonly columns: RA<string>;
  readonly treeInfo: TreeInfo | null;
};

/*
 * Indicates that a value had to be added to a picklist during uploading
 * a record
 */
type PicklistAddition = {
  // The new picklistitem id
  readonly id: number;
  // The name of the picklist receiving the new item
  readonly name: string;
  // The value of the new item
  readonly value: string;
  // The data set column that produced the new item
  readonly caption: string;
};

// Indicates that a new row was added to the database
type Uploaded = State<
  'Uploaded',
  {
    // The database id of the added row
    readonly id: number;
    readonly picklistAdditions: RA<PicklistAddition>;
    readonly info: ReportInfo;
  }
>;

// Indicates that an existing record in the database was matched
type Matched = State<
  'Matched',
  {
    // The id of the matched database row
    readonly id: number;
    readonly info: ReportInfo;
  }
>;

// Indicates failure due to finding multiple matches to existing records
type MatchedMultiple = State<
  'MatchedMultiple',
  {
    // List of ids of the matching database records
    readonly ids: RA<number>;
    readonly key: string;
    readonly info: ReportInfo;
  }
>;

/*
 * Indicates that no record was uploaded because all relevant columns in
 * the data set are empty
 */
type NullRecord = State<
  'NullRecord',
  {
    readonly info: ReportInfo;
  }
>;

// Indicates a record didn't upload due to a business rule violation
type FailedBusinessRule = State<
  'FailedBusinessRule',
  {
    // The error message generated by the business rule exception
    readonly message: string;
    readonly payload?: IR<unknown>;
    readonly info: ReportInfo;
  }
>;

/*
 * Indicates failure due to inability to find an expected existing
 * matching record
 */
type NoMatch = State<
  'NoMatch',
  {
    readonly info: ReportInfo;
  }
>;

/*
 * Indicates one or more values were invalid, preventing a record
 * from uploading
 */
type ParseFailures = State<
  'ParseFailures',
  {
    readonly failures: RA<
      readonly [string, IR<unknown>, string] | readonly [string, string]
    >;
  }
>;

// Indicates failure due to a failure to upload a related record
type PropagatedFailure = State<'PropagatedFailure'>;

type RecordResultTypes =
  | FailedBusinessRule
  | Matched
  | MatchedMultiple
  | NoMatch
  | NullRecord
  | ParseFailures
  | PropagatedFailure
  | Uploaded;

// Records the specific result of attempting to upload a particular record
type WbRecordResult = {
  readonly [recordResultType in RecordResultTypes['type']]: Omit<
    Extract<RecordResultTypes, State<recordResultType>>,
    'type'
  >;
};

export type UploadResult = {
  readonly UploadResult: {
    readonly record_result: WbRecordResult;
    /*
     * Maps the names of -to-one relationships of the table to upload
     * results for each
     * 'parent' exists for tree nodes only
     */
    readonly toOne: RR<string | 'parent', UploadResult>;
    /*
     * Maps the names of -to-many relationships of the table to an
     * array of upload results for each
     */
    readonly toMany: IR<RA<UploadResult>>;
  };
};

export function resolveBackendParsingMessage(
  key: string,
  payload: IR<unknown>
): LocalizedString | undefined {
  if (key === 'failedParsingBoolean')
    return backEndText.failedParsingBoolean({ value: payload.value as string });
  else if (key === 'failedParsingDecimal')
    return backEndText.failedParsingDecimal({ value: payload.value as string });
  else if (key === 'failedParsingFloat')
    return backEndText.failedParsingFloat({ value: payload.value as string });
  else if (key === 'failedParsingAgentType')
    return backEndText.failedParsingAgentType({
      agentTypeField: getField(tables.Agent, 'agentType').label,
      badType: payload.badType as string,
      validTypes: formatDisjunction(
        (payload.validTypes as RA<LocalizedString>) ?? []
      ),
    });
  else if (key === 'valueTooLong')
    return backEndText.valueTooLong({
      maxLength: payload.maxLength as number,
    });
  else if (key === 'invalidYear')
    return backEndText.invalidYear({
      value: payload.value as string,
    });
  else if (key === 'badDateFormat')
    return backEndText.badDateFormat({
      value: payload.value as string,
      format: payload.format as string,
    });
  else if (key === 'coordinateBadFormat')
    return backEndText.coordinateBadFormat({
      value: payload.value as string,
    });
  else if (key === 'latitudeOutOfRange')
    return backEndText.latitudeOutOfRange({
      value: payload.value as string,
    });
  else if (key === 'longitudeOutOfRange')
    return backEndText.longitudeOutOfRange({
      value: payload.value as string,
    });
  else if (key === 'formatMismatch')
    return backEndText.formatMismatch({
      value: payload.value as string,
      formatter: payload.formatter as string,
    });
  else return undefined;
}

/** Back-end sends a validation key. Front-end translates it */
export function resolveValidationMessage(
  key: string,
  payload: IR<unknown>
): LocalizedString {
  const baseParsedMessage = resolveBackendParsingMessage(key, payload);
  if (baseParsedMessage !== undefined) {
    return baseParsedMessage;
  } else if (key === 'failedParsingPickList')
    return backEndText.failedParsingPickList({
      value: `"${payload.value as string}"`,
    });
  else if (key === 'pickListValueTooLong')
    return backEndText.pickListValueTooLong({
      pickListTable: tables.PickList.label,
      pickList: payload.pickList as string,
      maxLength: payload.maxLength as number,
    });
  else if (key === 'invalidPartialRecord')
    return backEndText.invalidPartialRecord({
      column: payload.column as string,
    });
  else if (key === 'fieldRequiredByUploadPlan')
    return backEndText.fieldRequiredByUploadPlan();
  else if (key === 'invalidTreeStructure')
    return backEndText.invalidTreeStructure();
  else if (key === 'missingRequiredTreeParent')
    return backEndText.missingRequiredTreeParent({
      names: formatConjunction((payload.names as RA<LocalizedString>) ?? []),
    });
  // This can happen for data sets created before 7.8.2
  else
    return localized(
      `${key}${
        Object.keys(payload).length === 0 ? '' : ` ${JSON.stringify(payload)}`
      }`
    );
}
