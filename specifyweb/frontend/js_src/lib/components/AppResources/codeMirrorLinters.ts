import { jsonParseLinter } from '@codemirror/lang-json';
import type { Diagnostic } from '@codemirror/lint';
import { linter } from '@codemirror/lint';
import type { Extension, Text } from '@codemirror/state';
import type { EditorView } from 'codemirror';

import type { RA } from '../../utils/types';
import { mappedFind } from '../../utils/utils';

export const createLinter =
  (handler: (view: EditorView) => RA<Diagnostic>) =>
  (handleChange: (results: RA<Diagnostic>) => void): Extension =>
    linter((view) => {
      const results = handler(view);
      handleChange(results);
      return results;
    });

export const xmlLinter = createLinter(({ state }) => {
  const parsed = parseXml(state.doc.toString());
  return typeof parsed === 'string' ? [formatXmlError(state.doc, parsed)] : [];
});

export const jsonLinter = createLinter(jsonParseLinter());

export const xmlToString = (xml: Node): string =>
  new XMLSerializer().serializeToString(xml);

export function parseXml(string: string): Document | string {
  const parsedXml = new window.DOMParser().parseFromString(string, 'text/xml');

  // Chrome, Safari
  const parseError =
    parsedXml.documentElement.getElementsByTagName('parsererror')[0];
  if (typeof parseError === 'object')
    return (parseError.children[1].textContent ?? parseError.innerHTML).trim();
  // Firefox
  else if (parsedXml.documentElement.tagName === 'parsererror')
    return (
      parsedXml.documentElement.childNodes[0].nodeValue ??
      parsedXml.documentElement.textContent ??
      parsedXml.documentElement.innerHTML
    ).trim();
  else return parsedXml;
}

export function strictParseXml(xml: string): Element {
  const parsed = parseXml(xml);
  if (typeof parsed === 'string') throw new Error(parsed);
  else return parsed.documentElement;
}

const xmlErrorParsers = [
  /(?<message>[^\n]+)\n[^\n]+\nLine Number (?<line>\d+), Column (?<column>\d+)/u,
  /error on line (?<line>\d+) at column (?<column>\d+): (?<message>[\s\S]*)/u,
];

const formatXmlError = (text: Text, error: string): Diagnostic =>
  mappedFind(xmlErrorParsers, (regex) => {
    const groups = regex.exec(error)?.groups;
    if (groups === undefined) return undefined;
    const { line, column, message } = groups;
    const lineDescriptor = text.line(Number.parseInt(line));
    const position = lineDescriptor.from - 1 + Number.parseInt(column);
    return {
      from: position,
      to: position,
      severity: 'error',
      message,
    };
  }) ?? { from: 0, to: 0, severity: 'error', message: error };
