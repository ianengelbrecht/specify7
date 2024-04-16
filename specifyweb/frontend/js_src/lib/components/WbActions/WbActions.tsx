import React from 'react';

import { commonText } from '../../localization/common';
import { wbText } from '../../localization/workbench';
import { Http } from '../../utils/ajax/definitions';
import { ping } from '../../utils/ajax/ping';
import { Button } from '../Atoms/Button';
import { Dialog } from '../Molecules/Dialog';
import type { Status } from '../WbPlanView/Wrapped';
import { CreateRecordSetButton } from '../WorkBench/RecordSet';
import { WbStatus as WbStatusComponent } from '../WorkBench/Status';
import type { WbStatus, Workbench } from '../WorkBench/WbView';
import type { Dataset } from '../WbPlanView/Wrapped';
import type { WbMapping } from '../WorkBench/mapping';
import { hasPermission } from '../Permissions/helpers';
import { userPreferences } from '../Preferences/userPreferences';
import { useBooleanState } from '../../hooks/useBooleanState';
import { WbResults } from './WbResults';
import { WbValidate } from './WbValidate';
import { WbRollback } from './WbRollback';
import { WbUpload } from './WbUpload';
import { WbRevert } from './WbRevert';
import { WbSave } from './WbSave';
import { GET } from '../../utils/utils';
import { ErrorBoundary } from '../Errors/ErrorBoundary';
import { LoadingContext } from '../Core/Contexts';
import { WbNoUploadPlan } from './WbNoUploadPlan';
import { WbCellCounts } from '../WorkBench/CellMeta';

export function useWbActions({
  datasetId,
  workbench,
  checkDeletedFail,
  onRefresh: handleRefresh,
  onOpenStatus: handleOpenStatus,
}: {
  readonly datasetId: number;
  readonly workbench: Workbench;
  readonly checkDeletedFail: (statusCode: number) => void;
  readonly onRefresh: () => void;
  readonly onOpenStatus: () => void;
}) {
  const modeRef = React.useRef<WbStatus | undefined>(undefined);
  const refreshInitiatorAborted = React.useRef<boolean>(false);
  const loading = React.useContext(LoadingContext);

  const startUpload = (newMode: WbStatus): void => {
    workbench.validation.stopLiveValidation();
    loading(
      ping(`/api/workbench/${newMode}/${datasetId}/`, {
        method: 'POST',
        expectedErrors: [Http.CONFLICT],
      })
        .then((statusCode): void => {
          checkDeletedFail(statusCode);
          checkConflictFail(statusCode);
        })
        .then(() => triggerStatusComponent(newMode))
    );
  };

  const triggerStatusComponent = (newMode: WbStatus): void => {
    modeRef.current = newMode;
    handleOpenStatus();
  };

  const checkConflictFail = (statusCode: number): boolean => {
    if (statusCode === Http.CONFLICT)
      /*
       * Upload/Validation/Un-Upload has been initialized by another session
       * Need to reload the page to display the new state
       */
      handleRefresh();
    return statusCode === Http.CONFLICT;
  };

  return {
    modeRef,
    refreshInitiatorAborted,
    startUpload,
    triggerStatusComponent,
  };
}

function getMessage(cellCounts: WbCellCounts, mode: WbStatus) {
  const messages = {
    validate:
      cellCounts.invalidCells === 0
        ? {
            header: wbText.validationNoErrors(),
            message: (
              <>
                {wbText.validationNoErrorsDescription()}
                <br />
                <br />
                {wbText.validationReEditWarning()}
              </>
            ),
          }
        : {
            header: wbText.validationErrors(),
            message: (
              <>
                {wbText.validationErrorsDescription()}
                <br />
                <br />
                {wbText.validationReEditWarning()}
              </>
            ),
          },
    upload:
      cellCounts.invalidCells === 0
        ? {
            header: wbText.uploadSuccessful(),
            message: wbText.uploadSuccessfulDescription(),
          }
        : {
            header: wbText.uploadErrors(),
            message: (
              <>
                {wbText.uploadErrorsDescription()}
                <br />
                <br />
                {wbText.uploadErrorsSecondDescription()}
              </>
            ),
          },
    unupload: {
      header: wbText.dataSetRollback(),
      message: wbText.dataSetRollbackDescription(),
    },
  };

  return messages[mode];
}

export function WbActions({
  dataset,
  hasUnsavedChanges,
  isUploaded,
  isResultsOpen,
  workbench,
  mappings,
  checkDeletedFail,
  onDatasetRefresh: handleRefresh,
  onSpreadsheetUpToDate: handleSpreadsheetUpToDate,
  onToggleResults,
}: {
  readonly dataset: Dataset;
  readonly hasUnsavedChanges: boolean;
  readonly isUploaded: boolean;
  readonly isResultsOpen: boolean;
  readonly workbench: Workbench;
  readonly mappings: WbMapping | undefined;
  readonly checkDeletedFail: (statusCode: number) => void;
  readonly onDatasetRefresh: () => void;
  readonly onSpreadsheetUpToDate: () => void;
  readonly onToggleResults: () => void;
}): JSX.Element {
  const [canLiveValidate] = userPreferences.use(
    'workBench',
    'general',
    'liveValidation'
  );
  const [noUploadPlan, openNoUploadPlan, closeNoUploadPlan] = useBooleanState();
  const [showStatus, openStatus, closeStatus] = useBooleanState();
  const [operationAborted, openAbortedMessage, closeAbortedMessage] =
    useBooleanState();
  const [operationCompleted, openOperationCompleted, closeOperationCompleted] =
    useBooleanState();
  const { modeRef, refreshInitiatorAborted, ...actions } = useWbActions({
    datasetId: dataset.id,
    onRefresh: handleRefresh,
    checkDeletedFail,
    onOpenStatus: openStatus,
    workbench,
  });

  const cellCounts = workbench.cellCounts[GET];
  const message =
    modeRef.current === undefined
      ? undefined
      : getMessage(cellCounts, modeRef.current);

  return (
    <>
      <WbNoUploadPlan
        isUploaded={isUploaded}
        mappings={mappings}
        datasetId={dataset.id}
        noUploadPlan={noUploadPlan}
        onCloseNoUploadPlan={closeNoUploadPlan}
        onOpenNoUploadPlan={openNoUploadPlan}
      />
      {!isUploaded && hasPermission('/workbench/dataset', 'validate') ? (
        <ErrorBoundary dismissible>
          <WbValidate
            hasUnsavedChanges={hasUnsavedChanges}
            canLiveValidate={canLiveValidate}
            startUpload={actions.startUpload}
            validation={workbench.validation}
          />
        </ErrorBoundary>
      ) : undefined}
      <ErrorBoundary dismissible>
        <WbResults
          hasUnsavedChanges={hasUnsavedChanges}
          onToggleResults={onToggleResults}
          isResultsOpen={isResultsOpen}
        />
      </ErrorBoundary>
      {isUploaded && hasPermission('/workbench/dataset', 'unupload') ? (
        <ErrorBoundary dismissible>
          <WbRollback
            datasetId={dataset.id}
            triggerStatusComponent={actions.triggerStatusComponent}
          />
        </ErrorBoundary>
      ) : undefined}
      {!isUploaded && hasPermission('/workbench/dataset', 'upload') ? (
        <ErrorBoundary dismissible>
          <WbUpload
            hasUnsavedChanges={hasUnsavedChanges}
            mappings={mappings}
            openNoUploadPlan={openNoUploadPlan}
            startUpload={actions.startUpload}
            cellCounts={workbench.cellCounts[0]}
          />
        </ErrorBoundary>
      ) : undefined}
      {!isUploaded && hasPermission('/workbench/dataset', 'update') ? (
        <>
          <ErrorBoundary dismissible>
            <WbRevert
              hasUnsavedChanges={hasUnsavedChanges}
              onRefresh={handleRefresh}
              onSpreadsheetUpToDate={handleSpreadsheetUpToDate}
            />
          </ErrorBoundary>
          <ErrorBoundary dismissible>
            <WbSave
              hasUnsavedChanges={hasUnsavedChanges}
              onSpreadsheetUpToDate={handleSpreadsheetUpToDate}
              checkDeletedFail={checkDeletedFail}
              workbench={workbench}
            />
          </ErrorBoundary>
        </>
      ) : undefined}
      {typeof modeRef.current === 'string' && showStatus ? (
        <WbStatusComponent
          dataset={{
            ...dataset,
            // Create initial status if it doesn't exist yet
            uploaderstatus: {
              uploaderstatus:
                dataset.uploaderstatus ??
                ({
                  operation: {
                    validate: 'validating',
                    upload: 'uploading',
                    unupload: 'unuploading',
                  }[modeRef.current],
                  taskid: '',
                } as const),
              taskstatus: 'PENDING',
              taskinfo: 'None',
            } as Status,
          }}
          onFinished={(wasAborted): void => {
            refreshInitiatorAborted.current = wasAborted;
            closeStatus();
            if (wasAborted) openAbortedMessage();
            else openOperationCompleted();
            handleRefresh();
          }}
        />
      ) : undefined}
      {operationCompleted ? (
        <Dialog
          buttons={
            <>
              {cellCounts.invalidCells === 0 && modeRef.current === 'upload' && (
                <CreateRecordSetButton
                  datasetId={dataset.id}
                  datasetName={dataset.name}
                  small={false}
                  onClose={() => {
                    modeRef.current = undefined;
                    refreshInitiatorAborted.current = false;
                    closeOperationCompleted();
                  }}
                />
              )}
              <Button.DialogClose>{commonText.close()}</Button.DialogClose>
            </>
          }
          header={message!.header}
          onClose={closeOperationCompleted}
        >
          {message?.message}
        </Dialog>
      ) : undefined}
      {operationAborted ? (
        <Dialog
          buttons={commonText.close()}
          header={
            modeRef.current === 'validate'
              ? wbText.validationCanceled()
              : modeRef.current === 'unupload'
              ? wbText.rollbackCanceled()
              : wbText.uploadCanceled()
          }
          onClose={closeAbortedMessage}
        >
          {modeRef.current === 'validate'
            ? wbText.validationCanceledDescription()
            : modeRef.current === 'unupload'
            ? wbText.rollbackCanceledDescription()
            : wbText.uploadCanceledDescription()}
        </Dialog>
      ) : undefined}
    </>
  );
}
