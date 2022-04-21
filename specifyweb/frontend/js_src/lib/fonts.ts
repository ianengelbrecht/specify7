/**
 * Get fonts installed on user's computer
 * This can be replaced by navigator.fonts (the fonts API), once it launches
 */

/**
 * Source:
 * https://docs.microsoft.com/en-us/typography/fonts/windows_10_font_list
 *
 * The list was filtered down like this (on a Windows 10 machine):
 * ```js
 * macOsFonts.filter(f=>document.fonts.check(`12pt '${f}'`));
 * ```
 */
import { f } from './functools';
import { sortFunction } from './helpers';

const windowsFonts = [
  'Arial',
  'Arial Black',
  'Bahnschrift',
  'Calibri Light',
  'Calibri',
  'Cambria',
  'Cambria Math',
  'Candara Light',
  'Candara',
  'Comic Sans MS',
  'Consolas',
  'Constantia',
  'Corbel Light',
  'Corbel',
  'Courier New',
  'Ebrima',
  'Franklin Gothic Medium',
  'Gabriola',
  'Gadugi',
  'Georgia',
  'HoloLens MDL2 Assets',
  'Impact',
  'Ink Free',
  'Javanese Text',
  'Leelawadee UI',
  'Lucida Console',
  'Lucida Sans Unicode',
  'Malgun Gothic',
  'Marlett',
  'Microsoft Himalaya',
  'Microsoft JhengHei Light',
  'Microsoft JhengHei',
  'Microsoft JhengHei UI Light',
  'Microsoft JhengHei UI',
  'Microsoft New Tai Lue',
  'Microsoft PhagsPa',
  'Microsoft Sans Serif',
  'Microsoft Tai Le',
  'Microsoft YaHei Light',
  'Microsoft YaHei',
  'Microsoft YaHei UI Light',
  'Microsoft YaHei UI',
  'Microsoft Yi Baiti',
  'MingLiU-ExtB',
  'PMingLiU-ExtB',
  'MingLiU_HKSCS-ExtB',
  'Mongolian Baiti',
  'MS Gothic',
  'MS PGothic',
  'MS UI Gothic',
  'MV Boli',
  'Myanmar Text',
  'Nirmala UI',
  'Palatino Linotype',
  'Segoe MDL2 Assets',
  'Segoe Print',
  'Segoe Script',
  'Segoe UI Light',
  'Segoe UI',
  'Segoe UI Semibold',
  'Segoe UI Black',
  'Segoe UI Historic',
  'Segoe UI Emoji',
  'Segoe UI Symbol',
  'SimSun',
  'NSimSun',
  'SimSun-ExtB',
  'Sitka Small',
  'Sitka Text',
  'Sitka Subheading',
  'Sitka Heading',
  'Sitka Display',
  'Sitka Banner',
  'Sylfaen',
  'Symbol',
  'Tahoma',
  'Times New Roman',
  'Trebuchet MS',
  'Verdana',
  'Webdings',
  'Wingdings',
  'Yu Gothic Light',
  'Yu Gothic Regular',
  'Yu Gothic Medium',
  'Yu Gothic UI Light',
  'Yu Gothic UI Regular',
  'Yu Gothic UI Semibold',
];

/**
 * Source:
 * https://developer.apple.com/fonts/system-fonts/
 *
 * Fonts that are also present in windowsFonts were removed from the list
 * Also, the list was filtered down like this (on a mac):
 * ```js
 * macOsFonts.filter(fontName=>document.fonts.check(`12pt '${fontName}'`));
 * ```
 */
const macOsFonts = [
  'Al Nile',
  'American Typewriter',
  'Andale Mono',
  'Apple Braille',
  'Apple Chancery',
  'Apple Color Emoji',
  'Apple Symbols',
  'Arial Hebrew',
  'Arial Hebrew Scholar',
  'Arial Narrow',
  'Arial Rounded MT Bold',
  'Arial Unicode MS',
  'Avenir Black',
  'Avenir Black Oblique',
  'Avenir Book',
  'Avenir Heavy',
  'Avenir Light',
  'Avenir Medium',
  'Avenir Next Condensed Demi Bold',
  'Avenir Next Condensed Heavy',
  'Avenir Next Condensed Medium',
  'Avenir Next Condensed Ultra Light',
  'Avenir Next Demi Bold',
  'Avenir Next Heavy',
  'Avenir Next Medium',
  'Avenir Next Ultra Light',
  'Ayuthaya',
  'Bangla MN',
  'Bangla Sangam MN',
  'Baskerville',
  'Bodoni Ornaments',
  'Chalkboard',
  'Chalkduster',
  'Charter Black',
  'Cochin',
  'Copperplate',
  'Corsiva Hebrew',
  'Courier',
  'Devanagari MT',
  'Devanagari Sangam MN',
  'Didot',
  'Euphemia UCAS',
  'GB18030 Bitmap',
  'Galvji',
  'Geneva',
  'Gill Sans',
  'Gujarati MT',
  'Gujarati Sangam MN',
  'Gurmukhi MN',
  'Gurmukhi MT',
  'Gurmukhi Sangam MN',
  'Helvetica',
  'Helvetica Neue',
  'Herculanum',
  'Hiragino Maru Gothic ProN W4',
  'Hiragino Mincho ProN W3',
  'Hiragino Mincho ProN W6',
  'Hiragino Sans GB W3',
  'Hiragino Sans GB W6',
  'Hiragino Sans W0',
  'Hiragino Sans W1',
  'Hiragino Sans W2',
  'Hiragino Sans W3',
  'Hiragino Sans W4',
  'Hiragino Sans W5',
  'Hiragino Sans W6',
  'Hiragino Sans W7',
  'Hiragino Sans W8',
  'Hiragino Sans W9',
  'Hoefler Text',
  'Hoefler Text Ornaments',
  'InaiMathi',
  'Kannada MN',
  'Kannada Sangam MN',
  'Khmer MN',
  'Khmer Sangam MN',
  'Kohinoor Bangla',
  'Kohinoor Telugu',
  'Krungthep',
  'Lao MN',
  'Lao Sangam MN',
  'Lucida Grande',
  'Luminari',
  'Malayalam MN',
  'Malayalam Sangam MN',
  'Monaco',
  'Mshtakan',
  'MuktaMahee Bold',
  'MuktaMahee Light',
  'MuktaMahee Medium',
  'MuktaMahee Regular',
  'MuktaMahee SemiBold',
  'Myanmar MN',
  'Myanmar Sangam MN',
  'New Peninim MT',
  'Noto Nastaliq Urdu',
  'Noto Sans Kannada Black',
  'Noto Sans Kannada ExtraBold',
  'Noto Sans Kannada ExtraLight',
  'Noto Sans Kannada Light',
  'Noto Sans Kannada Medium',
  'Noto Sans Kannada SemiBold',
  'Noto Sans Kannada Thin',
  'Noto Sans Myanmar Light',
  'Noto Sans Myanmar Thin',
  'Noto Sans Oriya',
  'Oriya MN',
  'Oriya Sangam MN',
  'PT Mono',
  'PT Sans',
  'PT Sans Caption',
  'PT Sans Narrow',
  'PT Serif',
  'PT Serif Caption',
  'Palatino',
  'Papyrus',
  'Plantagenet Cherokee',
  'Raanana',
  'Rockwell',
  'STSong',
  'Sathu',
  'Shree Devanagari 714',
  'SignPainter-HouseScript',
  'Silom',
  'Sinhala MN',
  'Sinhala Sangam MN',
  'Snell Roundhand',
  'Tamil MN',
  'Tamil Sangam MN',
  'Telugu MN',
  'Telugu Sangam MN',
  'Thonburi',
  'Trattatello',
  'Wingdings 2',
  'Wingdings 3',
  'Zapf Dingbats',
  'Zapfino',
];

/**
 * Filter down the lists of fonts to match what user has installed
 *
 * @remarks
 * Adapted from https://stackoverflow.com/a/62755574/8584605
 */
export const getAvailableFonts = f.store(() =>
  Array.from(new Set([...windowsFonts, ...macOsFonts]))
    .sort(sortFunction<string, string>(f.id))
    .filter((fontName) => document.fonts.check(`12pt '${fontName}'`))
);
