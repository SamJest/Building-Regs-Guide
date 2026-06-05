export function breadcrumbForRoute(route) {
  const domain = 'https://buildingregsguide.co.uk';
  const item = (name, path) => ({ name, url: `${domain}${path}` });

  if (route.path === '/') return [item('Home', '/')];
  if (route.path.startsWith('/projects/')) return [item('Home', '/'), item('Projects', '/projects/'), item(route.title, route.path)];
  if (route.path.startsWith('/approved-documents/')) return [item('Home', '/'), item('Approved Documents', '/approved-documents/'), item(route.title, route.path)];
  if (route.path.startsWith('/tools/')) return [item('Home', '/'), item('Tools', '/tools/'), item(route.title, route.path)];
  if (route.path.startsWith('/downloads/')) return [item('Home', '/'), item('Downloads', '/downloads/'), item(route.title, route.path)];
  if (route.path.startsWith('/questions/')) return [item('Home', '/'), item('Questions', '/questions/'), item(route.title, route.path)];
  if (route.path.startsWith('/compare/')) return [item('Home', '/'), item('Compare', '/compare/'), item(route.title, route.path)];
  if (route.path.startsWith('/evidence/')) return [item('Home', '/'), item('Evidence', '/evidence/'), item(route.title, route.path)];
  return [item('Home', '/'), item(route.title, route.path)];
}
