import { error } from '../../components/Errors/assert';
import type { IR } from '../../utils/types';

const dictionary: IR<boolean> = {
  '((-webkit-backdrop-filter: none) or (backdrop-filter: none))': true,
};

Object.defineProperty(globalThis, 'CSS', {
  value: {
    supports: (query: string) =>
      dictionary[query] ?? error(`Unmocked CSS.supports query: ${query}`),
  },
});
