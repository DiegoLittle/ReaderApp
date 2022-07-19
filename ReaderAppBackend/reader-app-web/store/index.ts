import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit'
import settingsReducer from '../store/slices/settingsSlice'
import userLibraryReducer from '../store/slices/userLibrarySlice'
import pdfPageReducer from '../store/slices/pdfPageSlice'

export function makeStore() {

  return configureStore({
    reducer: { settings:settingsReducer,userLibrary:userLibraryReducer,pdfPage:pdfPageReducer },
  })
}

const store = makeStore()

export type AppState = ReturnType<typeof store.getState>

export type AppDispatch = typeof store.dispatch

export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  AppState,
  unknown,
  Action<string>
>

export default store