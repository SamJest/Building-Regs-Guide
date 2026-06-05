/**
 * Version guard for source-sensitive pages.
 * Codex should run this during build validation.
 */

export const SOURCE_VERSION_RULES = [
  {
    match_slug_contains: 'approved-document-l',
    required_source_ids: ['govuk_approved_document_l_2026', 'govuk_approved_documents_collection'],
    required_copy: 'Earlier versions of Approved Document L may continue to apply to buildings subject to previous regulatory standards.'
  },
  {
    match_slug_contains: 'higher-risk-buildings',
    required_source_ids: ['govuk_bsr_strategic_plan_2026_2027'],
    required_copy: 'BSR is the building control authority for higher-risk buildings in England.'
  },
  {
    match_page_type: 'approved_document_hub',
    required_source_ids: ['govuk_approved_documents_collection'],
    required_copy: 'Approved Documents provide guidance on ways to meet the building regulations.'
  }
];
