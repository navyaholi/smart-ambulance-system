
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const getPatients = () => api.get("/patients");

export const getAmbulances = () => api.get("/ambulances");

export const getHospitals = () => api.get("/hospitals");

export const getNearestAmbulance = (latitude, longitude) =>
  api.get("/ambulances/nearest", {
    params: { latitude, longitude },
  });

export const getSuitableHospital = (latitude, longitude) =>
  api.get("/hospitals/suitable", {
    params: { latitude, longitude },
  });

export const getRoute = (start, destination) =>
  api.get("/route", {
    params: { start, destination },
  });

export const allocateAmbulances = () => api.post("/allocate");

export default api;
