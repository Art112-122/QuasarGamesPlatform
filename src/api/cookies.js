import cookies from "js-cookie"

function getCookie(key) {
  return cookies.get(key);
}

function setCookie(key, value) {
  cookies.set(key, value);
}

function getToken() {
  return cookies.get('token');
}

export { getCookie, setCookie, getToken };
