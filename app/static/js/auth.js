function authorizedFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  const headers = options.headers || {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  options.headers = headers;
  options.credentials = "include"; // куки для SSR-частей, если есть

  return fetch(url, options);
}
