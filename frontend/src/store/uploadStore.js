import { create } from "zustand";

const useUploadStore = create((set) => ({
  files: [],

  setFiles: (files) =>
    set({
      files,
    }),

  addFile: (file) =>
    set((state) => ({
      files: [file, ...state.files],
    })),

  deleteFile: (id) =>
    set((state) => ({
      files: state.files.filter(
        (file) => file.id !== id
      ),
    })),
}));

export default useUploadStore;