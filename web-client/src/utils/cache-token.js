/** 统一处理 Cookie */

import Constants from "@/config";

export const getToken = () => {
  return sessionStorage.getItem(Constants.TOKEN);
};
export const setToken = token => {
  sessionStorage.setItem(Constants.TOKEN, token);
};
export const removeToken = () => {
  sessionStorage.removeItem(Constants.TOKEN);
};
