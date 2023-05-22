import React from 'react';
import { useOutletContext } from 'react-router';
import { useNavigate } from 'react-router-dom';
import type { LocalizedString } from 'typesafe-i18n';

import { useBooleanState } from '../../hooks/useBooleanState';
import { useId } from '../../hooks/useId';
import { commonText } from '../../localization/common';
import { resourcesText } from '../../localization/resources';
import { getUniqueName } from '../../utils/uniquifyName';
import { group } from '../../utils/utils';
import { Ul } from '../Atoms';
import { Button } from '../Atoms/Button';
import { className } from '../Atoms/className';
import { Form, Input, Label } from '../Atoms/Form';
import { Link } from '../Atoms/Link';
import { Submit } from '../Atoms/Submit';
import { LoadingContext, ReadOnlyContext } from '../Core/Contexts';
import type { SpecifyTable } from '../DataModel/specifyTable';
import type { ViewDefinition } from '../FormParse';
import { parseViewDefinition } from '../FormParse';
import { SpecifyForm } from '../Forms/SpecifyForm';
import { Dialog } from '../Molecules/Dialog';
import { resolveRelative } from '../Router/queryString';
import { createViewDefinition } from './createView';
import type { AllTableViews } from './fetchAllViews';
import { fetchAllViews } from './fetchAllViews';
import type { FormEditorOutlet } from './index';

export function CreateFormDefinition({
  table,
}: {
  readonly table: SpecifyTable;
}): JSX.Element {
  const [isCreating, handleCreating, handleNotCreating] = useBooleanState();
  const [views, setViews] = React.useState<AllTableViews | undefined>(
    undefined
  );
  const loading = React.useContext(LoadingContext);

  const [template, setTemplate] = React.useState<
    ViewDefinition | 'new' | undefined
  >(undefined);

  return (
    <>
      <div>
        <Button.Success
          onClick={(): void =>
            views === undefined
              ? loading(
                  fetchAllViews(table.name).then(setViews).then(handleCreating)
                )
              : handleCreating()
          }
        >
          {commonText.create()}
        </Button.Success>
      </div>
      {isCreating && typeof views === 'object' ? (
        <Dialog
          buttons={
            <>
              <Button.DialogClose>{commonText.cancel()}</Button.DialogClose>
              <Button.Info onClick={(): void => setTemplate('new')}>
                {commonText.new()}
              </Button.Info>
            </>
          }
          header={resourcesText.createNewForm()}
          onClose={handleNotCreating}
        >
          <div className="flex flex-col gap-8">
            <ListViews
              header={resourcesText.copyFromExistingForm()}
              table={table}
              views={views.database}
              onSelect={setTemplate}
            />
            <ListViews
              header={resourcesText.copyDefaultForm()}
              table={table}
              views={views.disk}
              onSelect={setTemplate}
            />
          </div>
        </Dialog>
      ) : undefined}
      {template !== undefined && (
        <ChooseName
          table={table}
          template={template}
          onClose={(): void => {
            setTemplate(undefined);
            handleNotCreating();
          }}
        />
      )}
    </>
  );
}

function ListViews({
  table,
  header,
  views,
  onSelect: handleSelect,
}: {
  readonly table: SpecifyTable;
  readonly header: LocalizedString;
  readonly views: AllTableViews['database'] | AllTableViews['disk'];
  readonly onSelect: (view: ViewDefinition) => void;
}): JSX.Element {
  const grouped = React.useMemo(
    () => group(views.map((view) => [view.category, view] as const)),
    [views]
  );
  const [preview, setPreview] = React.useState<ViewDefinition | undefined>(
    undefined
  );
  return (
    <div className="flex flex-col gap-4">
      <h3 className={className.headerPrimary}>{header}</h3>
      <div className="flex flex-col gap-2">
        {grouped.map(([category, views], index) => (
          <div className="flex flex-col gap-2" key={index}>
            <h4 className={className.headerGray}>{category}</h4>
            <Ul className="flex flex-col gap-2">
              {views.map((view, index) => (
                <li className="flex gap-2" key={index}>
                  <Button.LikeLink onClick={(): void => setPreview(view)}>
                    {view.name}
                  </Button.LikeLink>
                  {typeof view.editUrl === 'string' && (
                    <Link.Icon
                      className={className.dataEntryEdit}
                      href={view.editUrl}
                      icon="pencil"
                      title={commonText.edit()}
                    />
                  )}
                </li>
              ))}
            </Ul>
          </div>
        ))}
      </div>
      {typeof preview === 'object' && (
        <PreviewView
          table={table}
          view={preview}
          onClose={(): void => setPreview(undefined)}
          onSelect={(): void => handleSelect(preview)}
        />
      )}
    </div>
  );
}

export function PreviewView({
  table,
  view,
  onClose: handleClose,
  onSelect: handleSelect,
}: {
  readonly table: SpecifyTable;
  readonly view: ViewDefinition;
  readonly onClose: () => void;
  readonly onSelect: () => void;
}): JSX.Element {
  const resource = React.useMemo(() => new table.Resource(), [table]);
  const viewDefinition = React.useMemo(
    () => parseViewDefinition(view, 'form', 'edit', table),
    [view, table]
  );
  return (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText.close()}</Button.DialogClose>
          <Button.Info onClick={handleSelect}>
            {commonText.select()}
          </Button.Info>
        </>
      }
      header={`${resourcesText.preview()} ${view.name}`}
      onClose={handleClose}
    >
      <ReadOnlyContext.Provider value>
        <SpecifyForm
          display="block"
          resource={resource}
          viewDefinition={viewDefinition}
        />
      </ReadOnlyContext.Provider>
    </Dialog>
  );
}

function ChooseName({
  table,
  template,
  onClose: handleClose,
}: {
  readonly table: SpecifyTable;
  readonly template: ViewDefinition | 'new';
  readonly onClose: () => void;
}): JSX.Element {
  const id = useId('create-view')('');
  const {
    viewSets: [viewSets, setViewSets],
  } = useOutletContext<FormEditorOutlet>();

  const getUnique = (name: string): string =>
    getUniqueName(
      name,
      viewSets.views.map(({ name }) => name ?? ''),
      Number.POSITIVE_INFINITY,
      'name'
    );
  const [name, setName] = React.useState(() =>
    getUnique(template === 'new' ? table.name : template.name)
  );

  const navigate = useNavigate();
  return (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText.cancel()}</Button.DialogClose>
          <Submit.Info form={id}>{commonText.create()}</Submit.Info>
        </>
      }
      header={resourcesText.formDefinition()}
      onClose={handleClose}
    >
      <Form
        id={id}
        onSubmit={(): void => {
          const uniqueName = getUnique(name);
          setViewSets(
            createViewDefinition(viewSets, uniqueName, table, template),
            [uniqueName]
          );
          navigate(resolveRelative(`./${uniqueName}`));
        }}
      >
        <Label.Block>
          <Input.Text required value={name} onValueChange={setName} />
        </Label.Block>
      </Form>
    </Dialog>
  );
}
