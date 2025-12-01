import { defineStore } from "pinia";

export const useExperimentStore = defineStore("experiment", {
  state: () => ({
    experiment: null, //current experiment
    experiments: [],
    experimentType: null,
  }),

  actions: {
    setExperiment(experiment) {
      this.experiment = experiment;
    },
    setExperiments(experiments) {
      this.experiments = experiments;
    },
    setExperimentType(experimentType) {
      this.experimentType = experimentType;
    },
  },
  persist: true,
});
