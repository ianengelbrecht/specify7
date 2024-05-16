import React from 'react';
import type { LocalizedString } from 'typesafe-i18n';

import { commonText } from '../../localization/common';
import { headerText } from '../../localization/header';
import { localityText } from '../../localization/locality';
import { mainText } from '../../localization/main';
import { notificationsText } from '../../localization/notifications';
import { wbText } from '../../localization/workbench';
import { ajax } from '../../utils/ajax';
import { Http } from '../../utils/ajax/definitions';
import type { IR, RA } from '../../utils/types';
import { H2 } from '../Atoms';
import { Button } from '../Atoms/Button';
import { formatConjunction } from '../Atoms/Internationalization';
import { LoadingContext } from '../Core/Contexts';
import { tables } from '../DataModel/tables';
import type { Tables } from '../DataModel/types';
import { softFail } from '../Errors/Crash';
import { CsvFilePicker } from '../Molecules/CsvFilePicker';
import { Dialog } from '../Molecules/Dialog';
import { hasPermission, hasToolPermission } from '../Permissions/helpers';
import { ProtectedTool } from '../Permissions/PermissionDenied';
import { CreateRecordSet } from '../QueryBuilder/CreateRecordSet';
import { downloadDataSet } from '../WorkBench/helpers';
import { TableRecordCounts } from '../WorkBench/Results';
import { resolveBackendParsingMessage } from '../WorkBench/resultsParser';

type Header = Exclude<
  Lowercase<
    | keyof Tables['GeoCoordDetail']['fields']
    | keyof Tables['Locality']['fields']
  >,
  'locality'
>;

const acceptedLocalityFields: RA<
  Lowercase<keyof Tables['Locality']['fields']>
> = ['guid', 'datum', 'latitude1', 'longitude1'];

const acceptedHeaders = new Set([
  ...acceptedLocalityFields,
  ...tables.GeoCoordDetail.literalFields
    .map(({ name }) => name.toLowerCase())
    .filter((header) => header !== 'locality'),
]);

const requiredHeaders = new Set<Header>(['guid']);

type LocalityImportParseError = {
  readonly message: string;
  readonly payload: IR<unknown>;
  readonly rowNumber: number;
};

type LocalityUploadResponse =
  | {
      readonly type: 'ParseError';
      readonly data: RA<LocalityImportParseError>;
    }
  | {
      readonly type: 'Uploaded';
      readonly localities: RA<number>;
      readonly geocoorddetails: RA<number>;
    };

export function ImportLocalitySet(): JSX.Element {
  const [headerErrors, setHeaderErrors] = React.useState({
    missingRequiredHeaders: [] as RA<Header>,
    unrecognizedHeaders: [] as RA<string>,
  });

  const [headers, setHeaders] = React.useState<RA<string>>([]);
  const [data, setData] = React.useState<RA<RA<number | string>>>([]);
  const [results, setResults] = React.useState<
    LocalityUploadResponse | undefined
  >(undefined);

  const loading = React.useContext(LoadingContext);

  function resetContext(): void {
    setHeaderErrors({
      missingRequiredHeaders: [] as RA<Header>,
      unrecognizedHeaders: [] as RA<string>,
    });
    setHeaders([]);
    setData([]);
    setResults(undefined);
  }

  const handleImport = (
    columnHeaders: typeof headers,
    rows: typeof data
  ): void => {
    loading(
      ajax<LocalityUploadResponse>('/api/import/locality_set/', {
        headers: { Accept: 'application/json' },
        expectedErrors: [Http.UNPROCESSABLE],
        method: 'POST',
        body: {
          columnHeaders,
          data: rows,
        },
      }).then(({ data: rawData, status }) => {
        const data =
          status === 422 && typeof rawData === 'string'
            ? (JSON.parse(rawData) as LocalityUploadResponse)
            : rawData;
        setData([]);
        setResults(data);
      })
    );
  };

  return (
    <>
      <CsvFilePicker
        header={headerText.coGeImportDataset()}
        onFileImport={(headers, data): void => {
          const foundHeaderErrors = headers.reduce(
            (accumulator, currentHeader) => {
              const parsedHeader = currentHeader.toLowerCase().trim() as Header;
              const isUnknown = !acceptedHeaders.has(parsedHeader);

              return {
                missingRequiredHeaders:
                  accumulator.missingRequiredHeaders.filter(
                    (header) => header !== parsedHeader
                  ),
                unrecognizedHeaders: isUnknown
                  ? [...accumulator.unrecognizedHeaders, currentHeader]
                  : accumulator.unrecognizedHeaders,
              };
            },
            {
              missingRequiredHeaders: Array.from(requiredHeaders) as RA<Header>,
              unrecognizedHeaders: [] as RA<string>,
            }
          );
          setHeaderErrors(foundHeaderErrors);
          setHeaders(headers);
          setData(data);

          if (
            !Object.values(foundHeaderErrors).some(
              (errors) => errors.length > 0
            )
          )
            handleImport(headers, data);
        }}
      />
      {Object.values(headerErrors).some((errors) => errors.length > 0) && (
        <Dialog
          buttons={
            <>
              <Button.DialogClose>{commonText.close()}</Button.DialogClose>
              {headerErrors.missingRequiredHeaders.length === 0 && (
                <Button.Small onClick={(): void => handleImport(headers, data)}>
                  {commonText.import()}
                </Button.Small>
              )}
            </>
          }
          header={localityText.localityImportHeaderError()}
          icon={
            headerErrors.missingRequiredHeaders.length === 0
              ? 'warning'
              : 'error'
          }
          onClose={resetContext}
        >
          <>
            {headerErrors.missingRequiredHeaders.length > 0 && (
              <>
                <H2>{localityText.localityImportMissingHeader()}</H2>
                <p>
                  {formatConjunction(
                    headerErrors.missingRequiredHeaders as RA<LocalizedString>
                  )}
                </p>
              </>
            )}
            {headerErrors.unrecognizedHeaders.length > 0 && (
              <>
                <H2>{localityText.localityImportUnrecognizedHeaders()}</H2>
                <p>
                  {formatConjunction(
                    headerErrors.unrecognizedHeaders as RA<LocalizedString>
                  )}
                </p>
              </>
            )}
            <H2>{localityText.localityImportedAcceptedHeaders()}</H2>
            <p>
              {formatConjunction(
                Array.from(acceptedHeaders) as unknown as RA<LocalizedString>
              )}
            </p>
          </>
        </Dialog>
      )}
      {results === undefined ? null : (
        <LocalityImportResults results={results} onClose={resetContext} />
      )}
    </>
  );
}

function LocalityImportResults({
  results,
  onClose: handleClose,
}: {
  readonly results: LocalityUploadResponse;
  readonly onClose: () => void;
}): JSX.Element {
  return (
    <>
      {results.type === 'ParseError' ? (
        <LocalityImportErrors results={results} onClose={handleClose} />
      ) : results.type === 'Uploaded' ? (
        <Dialog
          buttons={
            <Button.DialogClose>{commonText.close()}</Button.DialogClose>
          }
          header={wbText.uploadResults()}
          modal={false}
          onClose={handleClose}
        >
          <div className="flex flex-col gap-4">
            <p>
              {localityText.localityUploadedDescription({
                localityTabelLabel: tables.Locality.label,
                geoCoordDetailTableLabel: tables.GeoCoordDetail.label,
              })}
            </p>
            <span className="gap-3" />
            <TableRecordCounts
              recordCounts={{
                locality: results.localities.length,
                geocoorddetail: results.geocoorddetails.length,
              }}
            />
            {hasToolPermission('recordSets', 'create') && (
              <CreateRecordSet
                baseTableName="Locality"
                recordIds={results.localities}
              />
            )}
          </div>
        </Dialog>
      ) : null}
    </>
  );
}

function LocalityImportErrors({
  results,
  onClose: handleClose,
}: {
  readonly results: Extract<
    LocalityUploadResponse,
    { readonly type: 'ParseError' }
  >;
  readonly onClose: () => void;
}): JSX.Element | null {
  const loading = React.useContext(LoadingContext);

  return (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText.close()}</Button.DialogClose>
          <Button.Info
            onClick={(): void => {
              const fileName = `${localityText.localityImportErrorFileName({
                date: new Date().toDateString(),
              })}.csv`;

              const columns = [
                localityText.rowNumber(),
                mainText.errorMessage(),
              ];

              const data = results.data.map(
                ({ message, payload, rowNumber }) => [
                  rowNumber.toString(),
                  resolveImportLocalityErrorMessage(message, payload),
                ]
              );

              loading(
                downloadDataSet(fileName, data, columns, ',').catch(softFail)
              );
            }}
          >
            {notificationsText.download()}
          </Button.Info>
        </>
      }
      header={localityText.localityImportErrorDialogHeader()}
      icon="error"
      onClose={handleClose}
    >
      <table className="grid-table grid-cols-[1fr_auto] gap-1 gap-y-3 overflow-auto">
        <thead>
          <tr>
            <td>{localityText.rowNumber()}</td>
            <td>{mainText.errorMessage()}</td>
          </tr>
        </thead>
        {results.data.map(({ rowNumber, message, payload }, index) => (
          <tr key={index}>
            <td>{rowNumber}</td>
            <td>{resolveImportLocalityErrorMessage(message, payload)}</td>
          </tr>
        ))}
      </table>
    </Dialog>
  );
}

function resolveImportLocalityErrorMessage(
  key: string,
  payload: IR<unknown>
): LocalizedString {
  const baseParseResults = resolveBackendParsingMessage(key, payload);

  if (baseParseResults !== undefined) {
    return baseParseResults;
  } else if (key === 'guidHeaderNotProvided') {
    return localityText.guidHeaderNotProvided();
  } else if (key === 'noLocalityMatchingGuid') {
    return localityText.noLocalityMatchingGuid({
      guid: payload.guid as string,
    });
  } else if (key === 'multipleLocalitiesWithGuid') {
    return localityText.multipleLocalitiesWithGuid({
      guid: payload.guid as string,
      localityIds: (payload.localityIds as RA<number>).join(', '),
    });
  } else {
    return commonText.colonLine({
      label: key,
      value:
        Object.keys(payload).length === 0 ? '' : `${JSON.stringify(payload)}`,
    });
  }
}
