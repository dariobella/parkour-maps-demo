import axios from 'axios'

let API_URL = 'http://127.0.0.1:8000/api'


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  U S E R S
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export function fetchMyUser(id) {
    return axios.get(`${API_URL}/user/${id}`)
}

export function addMyUser(user) {
    return axios.post(`${API_URL}/addUser/`, user)
}

export function updateMyUser(user, id) {
    return axios.put(`${API_URL}/user/${id}/`, user, { headers: {
            "Content-Type": "multipart/form-data",
        }})
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  S P O T S
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export function fetchSpots() {
    return axios.get(`${API_URL}/spots/`)
}

export function addSpot(spot) {
    return axios.post(`${API_URL}/spots/`, spot)
}

export function updateSpot(spot, id) {
    return axios.put(`${API_URL}/spots/${id}/`, spot)
}

export function deleteSpot(id) {
    return axios.delete(`${API_URL}/spots/${id}/`)
}

export function toggleFavourite(spot, user) {
    return axios.post(`${API_URL}/toggleFavourite/${spot}/`, user)
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  P I C S
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export function addPics(pics) {
    return axios.post(`${API_URL}/addPics/`, pics, { headers: {
            "Content-Type": "multipart/form-data",
        }})
}

export function spotPics(id) {
    return axios.get(`${API_URL}/spotPics/${id}/`)
}

export function updateSpotPics(id, data) {
    return axios.post(`${API_URL}/updateSpotPics/${id}/`, data,{ headers: {
            "Content-Type": "multipart/form-data",
        }})
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  M A P S
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export function fetchMaps(idUser) {
    return axios.get(`${API_URL}/myMaps/${idUser}/`)
}

export function loadMap(id) {
    return axios.get(`${API_URL}/map/${id}/`)
}

export function addMap(map, idUser) {
    return axios.post(`${API_URL}/addMap/${idUser}/`, map)
}

export function deleteMap(idUser, map) {
    return axios.delete(`${API_URL}/deleteMap/${idUser}/${map}`)
}

export function addSpotToMap(idUser, spot, map) {
    return axios.post(`${API_URL}/addSpotToMap/${idUser}/`, {spot, map})
}

export function deleteSpotFromMap(idUser, spot, map) {
    return axios.delete(`${API_URL}/deleteSpotFromMap/${idUser}/${spot}/${map}/`)
}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  A U T H
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export function fetchMe() {
    return axios.get(`${API_URL}/v1/users/me/`)
}

export function addUser(user) {
    return axios.post(`${API_URL}/v1/users/`, user)
}

export function login(user) {
  return axios.post(`${API_URL}/v1/token/login/`, user)
}

