import { createAsyncThunk, createSlice, current, PayloadAction } from '@reduxjs/toolkit'

import type { AppState, AppThunk } from '../index'

interface link {
  span: string
  link: {
    name: string
    type: string
    source: string
  }
  pages: number[]
}

export interface CounterState {
  currentPage: number
  links: link[]
}

const initialState: CounterState = {
  currentPage: 1,
  links: [],
}

export const pdfPageSlice = createSlice({
  name: 'pdfPage',
  initialState,
  // The `reducers` field lets us define reducers and generate associated actions
  reducers: {
    setCurrentPage: (state,action) => {
        state.currentPage = action.payload
    },
    setLinksRedux: (state,action) => {
      state.links = action.payload
    },
    addPageIndexToEntities: (state,action) =>{ 
      let entities = action.payload.entities
      let page = action.payload.page
      let links = state.links
      // console.log(page)
      // for each entity found in the page
      // loop through the links
      // 
      for (let i = 0; i < entities.length; i++) {
        let entity = entities[i]
        // console.log(entity)
        // for each link
        for (let j = 0; j < links.length; j++) {
          let link = links[j]
          // console.log(link.span.toLowerCase().trim())
          // console.log(entity.toLowerCase())
          // console.log(link.span.toLowerCase().trim() === entity.toLowerCase())
          // if the link spans the entity
          if (link.span.toLowerCase().trim()=== entity.toLowerCase()) {
            // add the page to the link if it is not already there
            if (!link.pages.includes(page)) {

              console.log(`adding page ${page} to link ${link.link.name} for found entity ${entity}`)

              link.pages.push(page)
            }
            links[j] = link
            // console.log(link)
          }
        }
      }
      state.links = links
      // current(state.links).forEach((link)=>{
      //   // console.log(link)
      //   if(link.pages.length > 0){
      //     console.log(link)
      //     console.log(link.pages)
      //   }
      // })
    }


  },
  // The `extraReducers` field lets the slice handle actions defined elsewhere,
  // including actions generated by createAsyncThunk or in other slices.
})

export const { setCurrentPage,setLinksRedux,addPageIndexToEntities } = pdfPageSlice.actions

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state: RootState) => state.counter.value)`
export const selectPdfPage = (state: AppState) => state.pdfPage

// We can also write thunks by hand, which may contain both sync and async logic.
// Here's an example of conditionally dispatching actions based on current state.


export default pdfPageSlice.reducer