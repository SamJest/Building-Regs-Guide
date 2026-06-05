export function smokeTestJsonLd(schemaObjects) {
  const errors = [];
  const schemas = Array.isArray(schemaObjects) ? schemaObjects : [schemaObjects];
  schemas.forEach((schema, index) => {
    if (!schema || typeof schema !== 'object') errors.push(`Schema ${index} is not an object`);
    if (!schema['@context']) errors.push(`Schema ${index} missing @context`);
    if (!schema['@type']) errors.push(`Schema ${index} missing @type`);
    const serialized = JSON.stringify(schema);
    if (serialized.includes('{{') || serialized.includes('}}')) errors.push(`Schema ${index} has unresolved template placeholders`);
    if (serialized.includes('undefined')) errors.push(`Schema ${index} contains undefined`);
  });
  return { valid: errors.length === 0, errors };
}

export function parseScriptContent(scriptText) {
  try {
    return { valid: true, parsed: JSON.parse(scriptText), errors: [] };
  } catch (error) {
    return { valid: false, parsed: null, errors: [error.message] };
  }
}
