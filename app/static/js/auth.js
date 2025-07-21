function authorizedFetch(url, options = {}) {
  options.credentials = "include";
  options.headers = options.headers || {};
  return fetch(url, options);
}
