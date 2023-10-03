import React from 'react';
import { useParams } from 'react-router-dom';
import type { LocalizedString } from 'typesafe-i18n';

import { useSearchParameter } from '../../hooks/navigation';
import { useAsyncState } from '../../hooks/useAsyncState';
import { useBooleanState } from '../../hooks/useBooleanState';
import { useCachedState } from '../../hooks/useCachedState';
import { useId } from '../../hooks/useId';
import { commonText } from '../../localization/common';
import { mergingText } from '../../localization/merging';
import { treeText } from '../../localization/tree';
import { ajax } from '../../utils/ajax';
import { Http } from '../../utils/ajax/definitions';
import { f } from '../../utils/functools';
import type { RA } from '../../utils/types';
import { filterArray } from '../../utils/types';
import { multiSortFunction, removeKey } from '../../utils/utils';
import { Button } from '../Atoms/Button';
import { Input, Label } from '../Atoms/Form';
import { icons } from '../Atoms/Icons';
import { Link } from '../Atoms/Link';
import { LoadingContext } from '../Core/Contexts';
import type { AnySchema, SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
<<<<<<< HEAD
import { fetchResource, resourceEvents } from '../DataModel/resource';
import { deserializeResource } from '../DataModel/serializers';
import type { SpecifyTable } from '../DataModel/specifyTable';
import { getTable } from '../DataModel/tables';
import type { Tables } from '../DataModel/types';
import { SaveButton } from '../Forms/Save';
import { Dialog } from '../Molecules/Dialog';
=======
import {
  fetchResource,
  resourceEvents,
  resourceOn,
} from '../DataModel/resource';
import { getModel } from '../DataModel/schema';
import type { SpecifyModel } from '../DataModel/specifyModel';
import { SaveBlockedDialog } from '../Forms/Save';
import { Dialog, dialogClassNames } from '../Molecules/Dialog';
>>>>>>> origin/production
import { userPreferences } from '../Preferences/userPreferences';
import { formatUrl } from '../Router/queryString';
import { OverlayContext, OverlayLocation } from '../Router/Router';
import { autoMerge } from './autoMerge';
import { CompareRecords } from './Compare';
<<<<<<< HEAD

const recordMergingTables = new Set<keyof Tables>(['Agent']);
=======
import { recordMergingTableSpec } from './definitions';
import { InvalidMergeRecordsDialog } from './InvalidMergeRecords';
import { Status } from './Status';
>>>>>>> origin/production

export const mergingQueryParameter = 'records';

export function RecordMergingLink({
  table,
  selectedRows,
  // Called when merging dialog closed, only if some records were merged
  onMerged: handleMerged,
  onDeleted: handleDeleted,
}: {
  readonly table: SpecifyTable;
  readonly selectedRows: ReadonlySet<number>;
  readonly onMerged: () => void;
  readonly onDeleted: (resourceId: number) => void;
}): JSX.Element | null {
  const overlayLocation = React.useContext(OverlayLocation);
  const [records] = useSearchParameter(mergingQueryParameter, overlayLocation);
  const oldRecords = React.useRef(records);
  const needUpdateQueryResults = React.useRef(false);

  React.useEffect(() => {
    if (oldRecords.current === undefined && records !== undefined)
      needUpdateQueryResults.current = false;
    // Detect agent merging dialog getting closed after some records are merged
    else if (
      records === undefined &&
      oldRecords.current !== undefined &&
      needUpdateQueryResults.current
    )
      handleMerged();
    oldRecords.current = records;
  }, [records]);

  React.useEffect(
    () =>
      resourceEvents.on('deleted', (resource) => {
        needUpdateQueryResults.current = true;
        handleDeleted(resource.id);
      }),
    [handleDeleted]
  );

  return table.name in recordMergingTableSpec ? (
    selectedRows.size > 1 ? (
      <Link.Small
        href={formatUrl(`/specify/overlay/merge/${table.name}/`, {
          [mergingQueryParameter]: Array.from(selectedRows).join(','),
        })}
      >
        {mergingText.mergeRecords()}
      </Link.Small>
    ) : (
      <Button.Small onClick={undefined}>
        {mergingText.mergeRecords()}
      </Button.Small>
    )
  ) : null;
}

export function MergingDialog(): JSX.Element | null {
  const { tableName = '' } = useParams();
  const table = getTable(tableName);

  const [rawIds = '', setIds] = useSearchParameter(mergingQueryParameter);
  const ids = React.useMemo(
    () => filterArray(rawIds.split(',').map(f.parseInt)),
    [rawIds]
  );
  React.useEffect(
    () =>
      resourceEvents.on('deleted', (resource) =>
        setIds(ids.filter((id) => id !== resource.id).join(','))
      ),
    [ids, setIds]
  );

<<<<<<< HEAD
  const handleDismiss = (dismissedId: number): void =>
    setIds(ids.filter((id) => id !== dismissedId).join(','));

  return table === undefined ? null : (
    <Merging ids={ids} table={table} onDismiss={handleDismiss} />
  );
}

function Merging({
  table,
=======
  const handleDismiss = (dismissedIds: RA<number>) =>
    setIds(ids.filter((id) => !dismissedIds.includes(id)).join(','));

  return model === undefined ? null : (
    <RestrictMerge ids={ids} model={model} onDismiss={handleDismiss} />
  );
}

// FIXME: Remove this once bussinessrules issues have been figured out
function RestrictMerge({
  model,
>>>>>>> origin/production
  ids,
  onDismiss: handleDismiss,
}: {
  readonly table: SpecifyTable;
  readonly ids: RA<number>;
  readonly onDismiss: (ids: RA<number>) => void;
}): JSX.Element | null {
<<<<<<< HEAD
  const records = useResources(table, ids);
=======
  const records = useResources(model, ids);

>>>>>>> origin/production
  const initialRecords = React.useRef(records);
  if (initialRecords.current === undefined && records !== undefined)
    initialRecords.current = records;

  const recordsToIgnore = React.useMemo(
    () =>
      records === undefined
        ? undefined
        : filterArray(
            records.map((record) =>
              recordMergingTableSpec[model.name]?.filterIgnore?.(
                record as never
              )
            )
          ),
    [records]
  );

  return records === undefined ? null : recordsToIgnore !== undefined &&
    recordsToIgnore.length > 0 ? (
    <InvalidMergeRecordsDialog
      recordsToIgnore={recordsToIgnore as RA<SerializedResource<AnySchema>>}
      tableName={model.name}
      onDismiss={
        // Disable merging if less than 2 remaining
        records.length - recordsToIgnore.length >= 2 ? handleDismiss : undefined
      }
    />
  ) : (
    <Merging model={model} records={records} onDismiss={handleDismiss} />
  );
}

function Merging({
  model,
  records,
  onDismiss: handleDismiss,
}: {
  readonly model: SpecifyModel;
  readonly records: RA<SerializedResource<AnySchema>>;
  readonly onDismiss: (ids: RA<number>) => void;
}): JSX.Element | null {
  const initialRecords = React.useRef(records);
  const handleClose = React.useContext(OverlayContext);
  // Close the dialog when resources are deleted/unselected
  React.useEffect(
    () => (records.length < 2 ? handleClose() : undefined),
    [records, handleClose]
  );

<<<<<<< HEAD
  const [form, setForm] = React.useState<HTMLFormElement | null>(null);
  const formId = useId('merging')('form');

=======
  const id = useId('merging-dialog');
  const formId = id('form');
>>>>>>> origin/production
  const loading = React.useContext(LoadingContext);

  const [needUpdate, setNeedUpdate] = React.useState(false);

  const rawSpecifyResources = React.useMemo(
    () => records.map(deserializeResource),
    [records, needUpdate]
  );

  const sortedResources = React.useMemo(
    () =>
      /*
       * Use the oldest resource as base so as to preserve timestampCreated
       * and, presumably the longest auditing history. If specifyuser exist
       * for agents being merged, take the most recent agent with specify user.
       * Multiple agents with specify user isn't handled.
       */
      Array.from(rawSpecifyResources).sort(
        multiSortFunction(
          (resource) => resource.get('specifyUser') ?? '',
          true,
          (resource) => resource.get('timestampCreated')
        )
      ),
    [rawSpecifyResources]
  );

  const target = sortedResources[0];
  const clones = sortedResources.slice(1);

  const [merged, setMerged] = useAsyncState(
    React.useCallback(
      async () =>
        records === undefined || initialRecords.current === undefined
          ? undefined
          : autoMerge(
              table,
              initialRecords.current,
<<<<<<< HEAD
              userPreferences.get('recordMerging', 'behavior', 'autoPopulate')
            ).then((merged) => deserializeResource(merged)),
      [table, records]
=======
              autoMerge(
                model,
                initialRecords.current,
                userPreferences.get(
                  'recordMerging',
                  'behavior',
                  'autoPopulate'
                ),
                target.id
              )
            ).then((merged) =>
              deserializeResource(merged as SerializedResource<AnySchema>)
            ),
      [model, records]
>>>>>>> origin/production
    ),
    true
  );

  const [mergeId, setMergeId] = React.useState<string | undefined>(undefined);

  return merged === undefined ? null : (
    <MergeDialogContainer
      buttons={
        <>
          <Button.Success
            onClick={(): void =>
              loading(
<<<<<<< HEAD
                autoMerge(table, records, false)
                  .then((merged) => deserializeResource(merged))
=======
                postMergeResource(
                  records,
                  autoMerge(model, records, false, target.id)
                )
                  .then((merged) =>
                    deserializeResource(merged as SerializedResource<AnySchema>)
                  )
>>>>>>> origin/production
                  .then(setMerged)
              )
            }
          >
            {mergingText.autoPopulate()}
          </Button.Success>
          <ToggleMergeView />
          <span className="-ml-2 flex-1" />
          <Button.BorderedGray onClick={handleClose}>
            {commonText.cancel()}
          </Button.BorderedGray>
<<<<<<< HEAD
          <MergeButton form={form} mergeResource={merged} />
=======
          <MergeButton formId={formId} mergeResource={merged} />
>>>>>>> origin/production
        </>
      }
      onClose={handleClose}
    >
      {mergeId === undefined ? undefined : (
        <Status
          handleClose={() => {
            /*
             * Because we can not pass down anything from the Query Builder
             * as a prop, this is needed to rerun the query results once
             * the merge completes.
             * (the RecordMergingLink component is listening to the event)
             */
            for (const clone of clones) {
              resourceEvents.trigger('deleted', clone);
            }
            handleClose();
          }}
          mergingId={mergeId}
        />
      )}
      <CompareRecords
<<<<<<< HEAD
        formRef={setForm}
        id={formId}
        merged={merged}
        records={records}
        table={table}
=======
        formId={formId}
        merged={merged}
        model={model}
        resources={rawSpecifyResources}
>>>>>>> origin/production
        onDismiss={handleDismiss}
        onMerge={(): void => {
          target.bulkSet(removeKey(merged.toJSON(), 'version'));
          loading(
            ajax(
              `/api/specify/${table.name.toLowerCase()}/replace/${target.id}/`,
              {
                method: 'POST',
                headers: {
                  Accept: 'application/json',
                },
                body: {
                  old_record_ids: clones.map((clone) => clone.id),
                  new_record_data: merged.toJSON(),
                },
                expectedErrors: [Http.NOT_ALLOWED],
                errorMode: 'dismissible',
              }
<<<<<<< HEAD
            ).then((response) => {
              if (response.status === Http.NOT_ALLOWED) {
                setError(response.data);
                return;
              }
              for (const clone of clones)
                resourceEvents.trigger('deleted', clone);

              setError(undefined);
              handleClose();
=======
            ).then(({ data, response }) => {
              if (!response.ok) return;
              setMergeId(data);
>>>>>>> origin/production
            })
          );
          setNeedUpdate(!needUpdate);
        }}
      />
    </MergeDialogContainer>
  );
}

function MergeButton<SCHEMA extends AnySchema>({
<<<<<<< HEAD
  form,
  mergeResource,
}: {
  readonly form: HTMLFormElement | null;
  readonly mergeResource: SpecifyResource<SCHEMA>;
}): JSX.Element | null {
  return form === null ? null : (
    <SaveButton
      form={form}
      label={treeText.merge()}
      resource={mergeResource}
      // Prevent regular form submit in favor of our custom
      onSaving={(): false => {
        form.requestSubmit();
        return false;
      }}
    />
=======
  formId,
  mergeResource,
}: {
  readonly formId: string;
  readonly mergeResource: SpecifyResource<SCHEMA>;
}): JSX.Element {
  const [saveBlocked, setSaveBlocked] = React.useState(false);
  const [showSaveBlockedDialog, setShowBlockedDialog] = React.useState(false);
  const [
    warningDialog,
    _,
    handleCloseWarningDialog,
    handleToggleWarningDialog,
  ] = useBooleanState(false);

  React.useEffect(() => {
    setSaveBlocked(false);
    return resourceOn(
      mergeResource,
      'blockersChanged',
      (): void => {
        const onlyDeferredBlockers = Array.from(
          mergeResource.saveBlockers?.blockingResources ?? []
        ).every((resource) => resource.saveBlockers?.hasOnlyDeferredBlockers());
        setSaveBlocked(!onlyDeferredBlockers);
      },
      true
    );
  }, [mergeResource]);

  const [noShowWarning = false, setNoShowWarning] = useCachedState(
    'merging',
    'warningDialog'
  );

  return (
    <>
      {saveBlocked ? (
        <Button.Danger className="cursor-not-allowed" onClick={undefined}>
          {treeText.merge()}
        </Button.Danger>
      ) : (
        <>
          {noShowWarning ? (
            <Submit.Blue form={formId}>{treeText.merge()}</Submit.Blue>
          ) : (
            <Button.Info onClick={handleToggleWarningDialog}>
              {treeText.merge()}
            </Button.Info>
          )}
        </>
      )}
      {showSaveBlockedDialog && (
        <SaveBlockedDialog
          resource={mergeResource}
          onClose={(): void => setShowBlockedDialog(false)}
        />
      )}
      {warningDialog && (
        <Dialog
          buttons={
            <>
              <Button.Warning onClick={handleToggleWarningDialog}>
                {commonText.cancel()}
              </Button.Warning>
              <span className="-ml-2 flex-1" />
              <Label.Inline>
                <Input.Checkbox
                  checked={noShowWarning}
                  onValueChange={(): void => setNoShowWarning(!noShowWarning)}
                />
                {commonText.dontShowAgain()}
              </Label.Inline>
              <Button.Info
                onClick={(): void => {
                  handleCloseWarningDialog();
                  document.forms.namedItem(formId)?.requestSubmit();
                }}
              >
                {commonText.proceed()}
              </Button.Info>
            </>
          }
          className={{
            container: dialogClassNames.narrowContainer,
          }}
          dimensionsKey="merging-warning"
          header={mergingText.mergeRecords()}
          onClose={undefined}
        >
          {mergingText.warningMergeText()}
        </Dialog>
      )}
    </>
>>>>>>> origin/production
  );
}

export function MergeDialogContainer({
  children,
  buttons,
  header = mergingText.mergeRecords(),
  onClose: handleClose,
}: {
  readonly header?: LocalizedString;
  readonly children: React.ReactNode;
  readonly buttons: JSX.Element;
  readonly onClose: () => void;
}): JSX.Element {
  return (
    <Dialog
      buttons={buttons}
      icon={icons.cog}
      onClose={handleClose}
      header={header}
      // Disable gradient because table headers have solid backgrounds
      specialMode="noGradient"
    >
      {children}
    </Dialog>
  );
}

export function ToggleMergeView(): JSX.Element {
  const [showMatching = false, setShowMatching] = useCachedState(
    'merging',
    'showMatchingFields'
  );
  return (
    <Label.Inline>
      <Input.Checkbox
        checked={!showMatching}
        onValueChange={(checked): void => setShowMatching(!checked)}
      />
      {mergingText.showConflictingFieldsOnly()}
    </Label.Inline>
  );
}

function useResources(
  table: SpecifyTable,
  selectedRows: RA<number>
): RA<SerializedResource<AnySchema>> | undefined {
  /**
   * During merging, ids are removed from selectedRows one by one. Shouldn't
   * try to fetch all resources every time that happens
   */
  const cached = React.useRef<RA<SerializedResource<AnySchema>>>([]);
  return useAsyncState(
    React.useCallback(
      async () =>
        Promise.all(
          selectedRows.map(async (id) => {
            const resource = cached.current.find(
              (resource) => resource.id === id
            );
            return resource ?? fetchResource(table.name, id);
          })
        ).then((resources) => {
          cached.current = resources;
          return resources;
        }),
      [table, selectedRows]
    ),
    true
  )[0];
}
