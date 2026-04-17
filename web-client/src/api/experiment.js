import axios from "@/utils/axios";

export const getExperimentList = data => {
  return axios.get("/api/experiment/", data);
};

export const createExperiment = data => {
  return axios.post("/api/experiment/", data);
};

export const getExperimentDetail  = (experiment_id, data) => {
  return axios.get(`/api/experiment/${experiment_id}`, data);
};

export const delExperiment  = (data) => {
  return axios.del(`/api/experiment/`, data);
};

export const updateExperimentProfile  = (experiment_id, data) => {
  return axios.put(`/api/experiment/${experiment_id}`, data);
};

export const updateExperiment  = (experiment_id, data) => {
  return axios.post(`/api/experiment/${experiment_id}`, data);
};

export const getExperimentResult  = (experiment_id, data) => {
  return axios.get(`/api/experiment/${experiment_id}/result`, data);
};

export const getAssistants = (experiment_id, data) => { 
  return axios.post(`/api/experiment/${experiment_id}/assistants`, data);
};

export const getMutations  = (experiment_id, data) => {
  return axios.get(`/api/experiment/${experiment_id}/mutations`, data);
};

export const getAssistantList = (experiment_id, data) => { 
  return axios.get(`/api/experiment/${experiment_id}/assistants`, data);
};

export const getMutationPDB = (experiment_id, data) => { 
  return axios.get(`/api/experiment/${experiment_id}/mutations/pdb`, data);
};

export const pdb_fileUpload = (experiment_id, data) => { 
  return axios.post(`/api/experiment/${experiment_id}/pdb_file`, data, {url:"pur/contract/upload"});
};

export const get_pdb_file = (experiment_id) => { 
  return axios.get(`/api/experiment/${experiment_id}/pdb_file`, {}, { responseType: "blob" });
};

export const get_pdb_files = (experiment_id, data) => {
  return axios.get(`/api/experiment/${experiment_id}/pdb_files`, data);
};

export const pdb_fileValidation = (data) => { 
  return axios.post(`/api/experiment/validation/pdb_file`, data, {url:"pur/contract/upload"});
};

export const updateAssistants  = (experiment_id, data) => {
  return axios.put(`/api/experiment/${experiment_id}/assistants`, data);
};

export const slurm = (experiment_id,data) => { 
  return axios.post(`/api/experiment/${experiment_id}/slurm`, data);
};

export const deploy = (experiment_id, params = {}, config = {}) => { 
  return axios.get(
    `/api/experiment/${experiment_id}/deploy`,
    params,
    { responseType: "blob", ...config }
  );
};

export const deployAccre = (experiment_id, params = {}, config = {}) => {
  return axios.get(
    `/api/experiment/${experiment_id}/deploy/accre`,
    params,
    { responseType: "blob", ...config }
  );
};

export const downloadable = (experiment_id, params = {}, config = {}) => { 
  return axios.get(
    `/api/experiment/${experiment_id}/downloadable`,
    params,
    { responseType: "blob", ...config }
  );
};
