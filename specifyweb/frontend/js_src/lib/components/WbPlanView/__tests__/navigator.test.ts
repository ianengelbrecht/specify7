import type { LocalizedString } from 'typesafe-i18n';

import { requireContext } from '../../../tests/helpers';
import { theories } from '../../../tests/utils';
import { getMappingLineData } from '../navigator';
import { navigatorSpecs } from '../navigatorSpecs';

requireContext();

// TEST: break this test into smaller tests
theories(getMappingLineData, [
  {
    in: [
      {
        baseTableName: 'CollectionObject',
        mappingPath: ['determinations', '#1', 'taxon', '$Family', 'name'],
        showHiddenFields: false,
        generateFieldData: 'all',
        // FIXME: add a test for query builder spec
        spec: navigatorSpecs.wbPlanView,
      },
    ],
    out: [
      {
        customSelectSubtype: 'simple',
        selectLabel: 'Collection Object' as LocalizedString,
        fieldsData: {
          catalogNumber: {
            optionLabel: 'Cat #',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          catalogedDate: {
            optionLabel: 'Cat Date',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          reservedText: {
            optionLabel: 'CT Scan',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          guid: {
            optionLabel: 'GUID',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          leftSideRels: {
            isDefault: false,
            isEnabled: true,
            isHidden: false,
            isRelationship: true,
            isRequired: false,
            optionLabel: 'Left Side Rels',
            tableName: 'CollectionRelationship',
          },
          altCatalogNumber: {
            optionLabel: 'Prev/Exch #',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          projectNumber: {
            optionLabel: 'Project Number',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          remarks: {
            optionLabel: 'Remarks',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          reservedText2: {
            optionLabel: 'Reserved Text2',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          rightSideRels: {
            isDefault: false,
            isEnabled: true,
            isHidden: false,
            isRelationship: true,
            isRequired: false,
            optionLabel: 'Right Side Rels',
            tableName: 'CollectionRelationship',
          },
          fieldNumber: {
            optionLabel: 'Voucher',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          accession: {
            optionLabel: 'Accession #',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'Accession',
          },
          cataloger: {
            optionLabel: 'Cataloger',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'Agent',
          },
          collectionObjectAttribute: {
            optionLabel: 'Col Obj Attribute',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'CollectionObjectAttribute',
          },
          collectionObjectCitations: {
            optionLabel: 'Collection Object Citations',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'CollectionObjectCitation',
          },
          determinations: {
            optionLabel: 'Determinations',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: true,
            isRelationship: true,
            tableName: 'Determination',
          },
          dnaSequences: {
            optionLabel: 'DNA Sequences',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'DNASequence',
          },
          collectingEvent: {
            optionLabel: 'Field No: Locality',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'CollectingEvent',
          },
          collection: {
            isDefault: false,
            isEnabled: true,
            isHidden: false,
            isRelationship: true,
            isRequired: false,
            optionLabel: 'Collection',
            tableName: 'Collection',
          },
          collectionObjectAttachments: {
            isDefault: false,
            isEnabled: true,
            isHidden: false,
            isRelationship: true,
            isRequired: false,
            optionLabel: 'Collection Object Attachments',
            tableName: 'CollectionObjectAttachment',
          },
          preparations: {
            optionLabel: 'Preparations',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'Preparation',
          },
          voucherRelationships: {
            optionLabel: 'Voucher Relationships',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'VoucherRelationship',
          },
        },
        tableName: 'CollectionObject',
      },
      {
        customSelectSubtype: 'toMany',
        selectLabel: 'Determination' as LocalizedString,
        fieldsData: {
          '#1': {
            optionLabel: '#1',
            isRelationship: true,
            isDefault: true,
            tableName: 'Determination',
          },
          '#2': {
            optionLabel: 'Add',
            isRelationship: true,
            isDefault: false,
            tableName: 'Determination',
          },
        },
        tableName: 'Determination',
      },
      {
        customSelectSubtype: 'simple',
        selectLabel: 'Determination' as LocalizedString,
        fieldsData: {
          determinedDate: {
            optionLabel: 'Date',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          guid: {
            optionLabel: 'GUID',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          typeStatusName: {
            optionLabel: 'Type Status',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          determiner: {
            optionLabel: 'Determiner',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: true,
            tableName: 'Agent',
          },
          taxon: {
            optionLabel: 'Taxon',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: true,
            isRelationship: true,
            tableName: 'Taxon',
          },
        },
        tableName: 'Determination',
      },
      {
        customSelectSubtype: 'tree',
        selectLabel: 'Taxon' as LocalizedString,
        fieldsData: {
          $Kingdom: {
            optionLabel: 'Kingdom',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Phylum: {
            optionLabel: 'Phylum',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Class: {
            optionLabel: 'Class',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Order: {
            optionLabel: 'Order',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Family: {
            optionLabel: 'Family',
            isRelationship: true,
            isDefault: true,
            tableName: 'Taxon',
          },
          $Subfamily: {
            optionLabel: 'Subfamily',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Genus: {
            optionLabel: 'Genus',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Subgenus: {
            optionLabel: 'Subgenus',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Species: {
            optionLabel: 'Species',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
          $Subspecies: {
            optionLabel: 'Subspecies',
            isRelationship: true,
            isDefault: false,
            tableName: 'Taxon',
          },
        },
        tableName: 'Taxon',
      },
      {
        customSelectSubtype: 'simple',
        selectLabel: 'Taxon' as LocalizedString,
        fieldsData: {
          author: {
            optionLabel: 'Author',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          commonName: {
            optionLabel: 'Common Name',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          guid: {
            optionLabel: 'GUID',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          name: {
            optionLabel: 'Name',
            isEnabled: true,
            isRequired: true,
            isHidden: false,
            isDefault: true,
            isRelationship: false,
          },
          remarks: {
            optionLabel: 'Remarks',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
          source: {
            optionLabel: 'Source',
            isEnabled: true,
            isRequired: false,
            isHidden: false,
            isDefault: false,
            isRelationship: false,
          },
        },
        tableName: 'Taxon',
      },
    ],
  },
]);
