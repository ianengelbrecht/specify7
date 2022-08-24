import React from 'react';

import type { SpQuery } from '../datamodel';
import type { SpecifyResource } from '../legacytypes';
import { commonText } from '../localization/common';
import { queryText } from '../localization/query';
import { schema } from '../schema';
import { userInformation } from '../userinfo';
import { getUniqueName } from '../wbuniquifyname';
import { Button, Form, Input, Label, Submit } from './basic';
import { LoadingContext } from './contexts';
import { useId } from './hooks';
import { Dialog, dialogClassNames } from './modaldialog';

async function doSave(
  query: SpecifyResource<SpQuery>,
  name: string,
  isSaveAs: boolean
): Promise<number> {
  const clonedQuery = isSaveAs ? await query.clone() : query;
  clonedQuery.set('name', name.trim());

  if (isSaveAs) clonedQuery.set('specifyUser', userInformation.resource_uri);
  return clonedQuery
    .save({
      // This may happen in development because React renders each component twice
      errorOnAlreadySaving: false,
    })
    .then(() => clonedQuery.id);
}

export function QuerySaveDialog({
  isSaveAs,
  query,
  onClose: handleClose,
  onSaved: handleSaved,
}: {
  readonly isSaveAs: boolean;
  readonly query: SpecifyResource<SpQuery>;
  readonly onClose: () => void;
  readonly onSaved: (queryId: number) => void;
}): JSX.Element | null {
  const id = useId('id');
  const [name, setName] = React.useState<string>((): string =>
    isSaveAs
      ? getUniqueName(query.get('name'), [query.get('name')])
      : query.get('name')
  );

  const loading = React.useContext(LoadingContext);

  React.useEffect(() => {
    if (query.isNew() || isSaveAs) return;
    loading(doSave(query, name, isSaveAs).then(handleSaved));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return query.isNew() || isSaveAs ? (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText('close')}</Button.DialogClose>
          <Submit.Blue form={id('form')}>{commonText('save')}</Submit.Blue>
        </>
      }
      className={{
        container: dialogClassNames.narrowContainer,
      }}
      header={
        isSaveAs
          ? queryText('saveClonedQueryDialogHeader')
          : queryText('saveQueryDialogHeader')
      }
      onClose={handleClose}
    >
      <p>
        {isSaveAs
          ? queryText('saveClonedQueryDialogText')
          : queryText('saveQueryDialogText')}
      </p>
      <Form
        className="contents"
        id={id('form')}
        onSubmit={(): void =>
          loading(doSave(query, name, isSaveAs).then(handleSaved))
        }
      >
        <Label.Generic>
          {queryText('queryName')}
          <Input.Text
            autoComplete="on"
            maxLength={schema.models.SpQuery.getLiteralField('name')!.length}
            name="queryName"
            required
            spellCheck="true"
            value={name}
            onValueChange={setName}
          />
        </Label.Generic>
      </Form>
    </Dialog>
  ) : null;
}
