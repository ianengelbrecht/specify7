import type { State } from 'typesafe-reducer';

import { attachmentsText } from '../../localization/attachments';
import { commonText } from '../../localization/common';
import { formsText } from '../../localization/forms';
import { wbText } from '../../localization/workbench';
import { ajax, AjaxResponseObject } from '../../utils/ajax';
import type { RA, RR } from '../../utils/types';
import { defined, filterArray } from '../../utils/types';
import {
  insertItem,
  keysToLowerCase,
  mappedFind,
  replaceItem,
  stripFileExtension,
} from '../../utils/utils';
import { addMissingFields } from '../DataModel/addMissingFields';
import { deserializeResource, serializeResource } from '../DataModel/helpers';
import type { SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { schema } from '../DataModel/schema';
import type { SpQuery, Tables } from '../DataModel/types';
import type { UiFormatter } from '../Forms/uiFormatters';
import { formatterTypeMapper } from '../Forms/uiFormatters';
import { queryFieldFilters } from '../QueryBuilder/FieldFilter';
import { makeQueryField } from '../QueryBuilder/fromTree';
import type { QueryFieldWithPath } from '../Statistics/types';
import type { AttachmentUploadSpec } from './Import';
import { staticAttachmentImportPaths } from './importPaths';
import type {
  AttachmentStatus,
  PartialUploadableFileSpec,
  UnBoundFile,
} from './types';
import { SerializedModel } from '../DataModel/helperTypes';
import { CollectionObject } from '../DataModel/types';
import { Http } from '../../utils/ajax/definitions';

export type ResolvedAttachmentRecord =
  | State<
      'invalid' | 'valid',
      { readonly reason: keyof typeof keyLocalizationMapAttachment }
    >
  | State<'matched', { readonly id: number }>;

const resolveAttachmentMatch = (
  matchedId: RA<number>,
  disambiguated: number | undefined
): ResolvedAttachmentRecord =>
  matchedId.length === 0
    ? { type: 'invalid', reason: 'noMatch' }
    : matchedId.length > 1 && disambiguated === undefined
    ? {
        type: 'invalid',
        reason: 'multipleMatches',
      }
    : {
        type: 'matched',
        id: disambiguated ?? matchedId[0],
      };

export function resolveAttachmentRecord(
  matchedId: RA<number> | undefined,
  disambiguated: number | undefined,
  parsedName: string | undefined
): ResolvedAttachmentRecord {
  if (parsedName === undefined)
    return { type: 'invalid', reason: 'incorrectFormatter' };
  if (matchedId === undefined)
    return { type: 'valid', reason: 'correctlyFormatted' };
  return resolveAttachmentMatch(matchedId, disambiguated);
}

export const canDeleteAttachment = (
  uploadSpec: PartialUploadableFileSpec
): boolean =>
  uploadSpec.attachmentId !== undefined &&
  uploadSpec.matchedId !== undefined &&
  resolveAttachmentMatch(uploadSpec.matchedId, uploadSpec.disambiguated)
    .type === 'matched';

function generateInQueryResource(
  baseTable: keyof Tables,
  path: string,
  searchableList: RA<number | string | undefined>,
  queryName: string,
  additionalPaths: RA<QueryFieldWithPath> = []
): SpecifyResource<SpQuery> {
  const rawFields = [
    ...additionalPaths,
    {
      path,
      isDisplay: true,
      operStart: queryFieldFilters.in.id,
      startValue: filterArray(searchableList).join(','),
    },
  ];
  const queryField = rawFields.map(({ path, ...field }, index) =>
    serializeResource(
      makeQueryField(baseTable, path, { ...field, position: index })
    )
  );
  return deserializeResource(
    addMissingFields('SpQuery', {
      name: queryName,
      contextName: baseTable,
      contextTableId: schema.models[baseTable].tableId,
      countOnly: false,
      fields: queryField,
    })
  );
}

export async function validateAttachmentFiles(
  uploadableFiles: RA<PartialUploadableFileSpec>,
  uploadSpec: AttachmentUploadSpec,
  keepDisambiguation: boolean = false
): Promise<RA<PartialUploadableFileSpec>> {
  const { baseTable, path } =
    staticAttachmentImportPaths[uploadSpec.staticPathKey];

  const validationQueryResource = generateInQueryResource(
    baseTable,
    path,
    uploadableFiles.map(({ file }) => file?.parsedName),
    'Batch Attachment Upload'
  );
  const rawValidationResponse = await validationPromiseGenerator(
    validationQueryResource
  );
  const mappedResponse = rawValidationResponse.map(
    ({ targetId, restResult }) => {
      const rawResult = uploadSpec.formatQueryResults(restResult[0]);
      return rawResult === undefined ? undefined : { targetId, rawResult };
    }
  );

  return matchFileSpec(
    uploadableFiles,
    filterArray(mappedResponse),
    keepDisambiguation
  );
}

type MatchSelectedFiles = {
  readonly resolvedFiles: RA<PartialUploadableFileSpec>;
  readonly duplicateFiles: RA<PartialUploadableFileSpec>;
};
export const matchSelectedFiles = (
  previousUploadables: RA<PartialUploadableFileSpec>,
  filesToResolve: RA<PartialUploadableFileSpec>
): MatchSelectedFiles =>
  filesToResolve.reduce<MatchSelectedFiles>(
    (previousMatchedSpec, uploadable) => {
      const matchedIndex = previousMatchedSpec.resolvedFiles.findIndex(
        (previousUploadable) =>
          previousUploadable.file !== undefined &&
          previousUploadable.file.name === uploadable.file.name &&
          previousUploadable.file.size === uploadable.file.size &&
          previousUploadable.file.type === uploadable.file.type
      );
      if (matchedIndex === -1)
        return {
          ...previousMatchedSpec,
          resolvedFiles: insertItem(
            previousMatchedSpec.resolvedFiles,
            previousMatchedSpec.resolvedFiles.length,
            uploadable
          ),
        };
      if (previousMatchedSpec.resolvedFiles[matchedIndex].file instanceof File)
        return {
          ...previousMatchedSpec,
          duplicateFiles: [...previousMatchedSpec.duplicateFiles, uploadable],
        };
      return {
        ...previousMatchedSpec,
        resolvedFiles: replaceItem(
          previousMatchedSpec.resolvedFiles,
          matchedIndex,
          {
            ...previousMatchedSpec.resolvedFiles[matchedIndex],
            file: uploadable.file,
            /*
             * Generating tokens again because the file could have been
             * uploaded to the asset server but not yet recorded in Specify DB.
             */
            uploadTokenSpec: undefined,
            // Take the new status in case of parse failure was reported.
            status: uploadable.status,
          }
        ),
      };
    },
    {
      resolvedFiles: previousUploadables,
      duplicateFiles: [],
    }
  );

export function resolveFileNames(
  previousFile: UnBoundFile,
  getFormatted: (rawName: number | string | undefined) => string | undefined,
  formatter?: UiFormatter
): PartialUploadableFileSpec {
  const splitName = stripFileExtension(previousFile.name);
  let formatted = getFormatted(splitName);
  if (
    formatter?.fields.every(
      (field) => !(field instanceof formatterTypeMapper.regex)
    ) === true
  ) {
    const formattedLength = formatter.fields.reduce(
      (length, field) => length + field.size,
      0
    );
    formatted =
      getFormatted(previousFile.name.slice(0, formattedLength)) ?? formatted;
  }
  previousFile.parsedName = formatted;

  return {
    file: previousFile,
  };
}

const validationPromiseGenerator = async (
  queryResource: SpecifyResource<SpQuery>
): Promise<
  RA<{
    readonly targetId: number;
    readonly restResult: RA<number | string>;
  }>
> =>
  ajax<{
    // First value is the primary key
    readonly results: RA<readonly [number, ...RA<number | string>]>;
  }>('/stored_query/ephemeral/', {
    method: 'POST',
    headers: {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      Accept: 'application/json',
    },
    body: keysToLowerCase({
      ...serializeResource(queryResource),
      countOnly: false,
      limit: 0,
    }),
  }).then(({ data }) =>
    data.results.map(([target, ...restResult]) => ({
      targetId: target,
      restResult,
    }))
  );

const matchFileSpec = (
  uploadFileSpec: RA<PartialUploadableFileSpec>,
  queryResults: RA<{
    readonly targetId: number;
    readonly rawResult: string;
  }>,
  keepDisambiguation: boolean = false
): RA<PartialUploadableFileSpec> =>
  uploadFileSpec.map((spec) => {
    const specParsedName = spec.file?.parsedName;
    // Don't match files already uploaded.
    if (specParsedName === undefined || typeof spec.attachmentId === 'number')
      return spec;
    const matchingResults = queryResults.filter(
      (result) => result.rawResult === specParsedName
    );
    const newSpec: PartialUploadableFileSpec = {
      ...spec,
      matchedId: matchingResults.map((result) => result.targetId),
    };

    if (
      keepDisambiguation &&
      spec.disambiguated !== undefined &&
      // If disambiguation was chosen, but it became invalid, reset disambiguation
      newSpec.matchedId?.includes(spec.disambiguated) === true
    ) {
      return newSpec;
    }
    return { ...newSpec, disambiguated: undefined };
  });

export async function reconstructDeletingAttachment(
  staticKey: keyof typeof staticAttachmentImportPaths,
  deletableFiles: RA<PartialUploadableFileSpec>
): Promise<RA<PartialUploadableFileSpec>> {
  const baseTable = staticAttachmentImportPaths[staticKey].baseTable;
  const relationshipName = `${baseTable}attachments`;
  const attachmentTableId = `${baseTable}attachmentid`;
  const path = `${relationshipName}.${attachmentTableId}`;
  const relatedAttachments = filterArray(
    deletableFiles.map((deletable) =>
      deletable.status?.type === 'matched' ? deletable.attachmentId : undefined
    )
  );
  const reconstructingQueryResource = generateInQueryResource(
    baseTable,
    path,
    relatedAttachments,
    'Batch Attachment Upload'
  );
  const queryResults = await validationPromiseGenerator(
    reconstructingQueryResource
  );
  return deletableFiles.map((deletable) => {
    if (deletable.status?.type !== 'matched') return deletable;
    const matchedId = deletable.status.id;
    const foundInQueryResult = queryResults.find(
      ({ targetId, restResult: [attachmentId] }) =>
        targetId === matchedId && attachmentId === deletable.attachmentId
    );
    return {
      ...deletable,
      attachmentId: foundInQueryResult?.restResult[0] as number,
      status:
        foundInQueryResult === undefined
          ? ({ type: 'success', successType: 'deleted' } as const)
          : deletable.status.type === 'matched'
          ? ({
              type: 'cancelled',
              reason: 'rollbackInterruption',
            } as const)
          : deletable.status,
    };
  });
}
export async function reconstructUploadingAttachmentSpec(
  staticKey: keyof typeof staticAttachmentImportPaths,
  uploadableFiles: RA<PartialUploadableFileSpec>
): Promise<RA<PartialUploadableFileSpec>> {
  const baseTable = staticAttachmentImportPaths[staticKey].baseTable;
  const relationshipName = `${baseTable}attachments`;
  const pathToAttachmentLocation = `${relationshipName}.attachment.attachmentLocation`;
  const attachmentTableId = `${relationshipName}.${baseTable}attachmentid`;
  const filteredAttachmentLocations = filterArray(
    uploadableFiles.map((uploadable) =>
      uploadable.status?.type === 'matched'
        ? uploadable.uploadTokenSpec?.attachmentLocation
        : undefined
    )
  );
  const reconstructingQueryResource = generateInQueryResource(
    baseTable,
    pathToAttachmentLocation,
    filteredAttachmentLocations,
    'Batch Attachment Upload',
    [
      {
        path: attachmentTableId,
        isDisplay: true,
        id: queryFieldFilters.any.id,
      },
    ]
  );
  const queryResults = await validationPromiseGenerator(
    reconstructingQueryResource
  );
  return uploadableFiles.map((uploadable) => {
    if (uploadable.status?.type !== 'matched') return uploadable;
    const matchedId = uploadable.status.id;
    const foundInQueryResult = queryResults.find(
      ({ targetId, restResult: [_, attachmentLocation] }) =>
        typeof attachmentLocation === 'string' &&
        targetId === matchedId &&
        attachmentLocation.toString() ===
          uploadable.uploadTokenSpec!.attachmentLocation
    );

    return {
      ...uploadable,
      attachmentId: foundInQueryResult?.restResult[0] as number,
      status:
        typeof foundInQueryResult === 'object'
          ? ({ type: 'success', successType: 'uploaded' } as const)
          : uploadable.status.type === 'matched'
          ? ({
              type: 'cancelled',
              reason: 'uploadInterruption',
            } as const)
          : uploadable.status,
    };
  });
}

export const keyLocalizationMapAttachment = {
  incorrectFormatter: attachmentsText.incorrectFormatter(),
  noFile: attachmentsText.noFile(),
  uploaded: commonText.uploaded(),
  deleted: attachmentsText.deleted(),
  alreadyUploaded: attachmentsText.alreadyUploaded(),
  alreadyDeleted: attachmentsText.alreadyDeleted(),
  skipped: attachmentsText.skipped(),
  cancelled: attachmentsText.cancelled(),
  matchError: attachmentsText.matchError(),
  noAttachments: attachmentsText.noAttachments(),
  uploadInterruption: attachmentsText.frontEndInterruption({
    action: wbText.upload(),
  }),
  rollbackInterruption: attachmentsText.frontEndInterruption({
    action: wbText.rollback(),
  }),
  errorReadingFile: attachmentsText.errorReadingFile(),
  attachmentServerUnavailable: attachmentsText.attachmentServerUnavailable(),
  saveConflict: formsText.saveConflict(),
  unhandledFatalResourceError: attachmentsText.unhandledFatalResourceError(),
  nothingFound: formsText.nothingFound(),
  noMatch: attachmentsText.noMatch(),
  multipleMatches: attachmentsText.multipleMatches(),
  correctlyFormatted: attachmentsText.correctlyFormatted(),
  userStopped: attachmentsText.stoppedByUser(),
  errorFetchingRecord: attachmentsText.errorFetchingRecord(),
  saveError: attachmentsText.errorSavingRecord(),
} as const;

export function resolveAttachmentStatus(
  attachmentStatus: AttachmentStatus
): string {
  if ('reason' in attachmentStatus) {
    const reason = keyLocalizationMapAttachment[attachmentStatus.reason];
    return commonText.colonLine({
      label: keyLocalizationMapAttachment[attachmentStatus.type],
      value: reason,
    });
  }
  return attachmentStatus.type === 'success'
    ? keyLocalizationMapAttachment[attachmentStatus.successType]
    : '';
}

export const getAttachmentsFromResource = (
  baseResource: SerializedResource<Tables['CollectionObject']>,
  relationshipName: string
): {
  readonly key: keyof SerializedResource<Tables['CollectionObject']>;
  readonly values: RA<SerializedResource<Tables['CollectionObjectAttachment']>>;
} =>
  defined(
    mappedFind(Object.entries(baseResource), ([key, value]) =>
      key.toLowerCase() === relationshipName.toLowerCase()
        ? {
            key,
            values: value as RA<
              SerializedResource<Tables['CollectionObjectAttachment']>
            >,
          }
        : undefined
    )
  );

type RecordResponse =
  | State<
      'invalid',
      { readonly reason: keyof typeof keyLocalizationMapAttachment }
    >
  | State<'valid', { readonly record: SerializedResource<CollectionObject> }>;

const wrapAjaxRecordResponse = async (
  ajaxPromise: () => Promise<
    AjaxResponseObject<SerializedModel<CollectionObject>>
  >,
  // Defines errors on which to not trigger a retry.
  statusMap: RR<number | 'fallback', keyof typeof keyLocalizationMapAttachment>,
  triggerRetry?: () => void
): Promise<RecordResponse> =>
  ajaxPromise().then(({ data, status }) => {
    if (statusMap[status] !== undefined)
      return { type: 'invalid', reason: statusMap[status] };
    if (status !== Http.OK) {
      triggerRetry?.();
      return { type: 'invalid', reason: statusMap.fallback };
    }
    return {
      type: 'valid',
      record: serializeResource(data),
    };
  });

const baseStatusMap = {
  [Http.NOT_FOUND]: 'nothingFound',
  [Http.CONFLICT]: 'saveConflict',
} as const;

export const fetchForAttachmentUpload = async (
  baseTableName: keyof Tables,
  matchId: number,
  triggerRetry?: () => void
) =>
  wrapAjaxRecordResponse(
    async () =>
      ajax<SerializedModel<CollectionObject>>(
        `/api/specify/${baseTableName.toLowerCase()}/${matchId}/`,
        { headers: { Accept: 'application/json' } },
        {
          expectedResponseCodes: Object.values(Http),
          strict: false,
        }
      ),
    { ...baseStatusMap, fallback: 'errorFetchingRecord' },
    triggerRetry
  );

export const saveForAttachmentUpload = async (
  baseTableName: keyof Tables,
  matchId: number,
  data: Partial<SerializedResource<CollectionObject>>,
  triggerRetry?: () => void
) =>
  wrapAjaxRecordResponse(
    async () =>
      ajax<SerializedModel<CollectionObject>>(
        `/api/specify/${baseTableName.toLowerCase()}/${matchId}/`,
        {
          method: 'PUT',
          body: keysToLowerCase(addMissingFields(baseTableName, data)),
          headers: { Accept: 'application/json' },
        },
        { expectedResponseCodes: Object.values(Http), strict: false }
      ),
    { ...baseStatusMap, fallback: 'saveError' },
    triggerRetry
  );
