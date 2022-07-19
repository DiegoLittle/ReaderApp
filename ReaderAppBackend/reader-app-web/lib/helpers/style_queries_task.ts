
import { css, cx } from '@emotion/css'

const style = css`
  color: hotpink;
`
const grid_style_lg = css`
  display: grid;
    grid-template-columns: repeat(12, minmax(0, 1fr))
  `
  const grid_style_xs = css`
  display: grid;
    grid-template-columns: repeat(12, minmax(0, 1fr))
  `
  const table_style_mobile = css`
  grid-column: span 12 / span 12
  `
  const table_style = css`
  grid-column: span 12 / span 12;
  width: 100%;
  `
  const infobox_style = css`
  grid-column: span 2 / span 2;
  `
  const infobox_style_mobile = css`
  grid-column: span 5
  `
  const description_style = css`
  grid-column: span 10 / span 10;`
  const description_style_mobile = css`
  grid-column: span 7 / span 7;`


export function get_page_styles(device_size){
    switch (device_size) {
        case 'xs':
          return {
              'grid':grid_style_xs,
              'table':table_style_mobile,
              'infobox':infobox_style_mobile,
              'description':description_style_mobile

          }
        case 'sm':
            return {
                'grid':grid_style_xs,
                'table':table_style_mobile,
                'infobox':infobox_style_mobile,
                'description':description_style_mobile
            }
        case 'md':
          return {
            'grid':grid_style_lg,
            'table':table_style_mobile,
            'infobox':infobox_style_mobile,
            'description':description_style_mobile
        }
        case 'lg':
            return {
                'grid':grid_style_lg,
                'table':table_style,
                'infobox':infobox_style,
                'description':description_style
            }
        case 'xl':
          return {
            'grid':grid_style_lg,
            'table':table_style,
            'infobox':infobox_style,
            'description':description_style
        }
        default:
          return {

          }
      }
}
// header: {
//     //         display: 'flex',
//     //         justifyContent: 'center',
//     //     },
//     //     body: {
//     //         boxShadow: '0px 0px 5px black',
//     //         display: 'flex',
//     //         justifyContent: 'center',
//     //         flexDirection: 'column'
//     //     }