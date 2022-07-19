//
//  SearchResults.swift
//  ReaderApp
//
//  Created by Diego Little on 4/30/22.
//

import Foundation
import SwiftUI
import FontAwesomeSwiftUI

struct searchResultsView: View{
    @State var query: String = ""
    @FocusState private var isFocused:Bool
    @EnvironmentObject var store: AppStore
    @ObservedObject var presenter: ContentPresenter



    var body: some View{
        List{
            ForEach(store.state.searchResults){ result in
                Button(action:{
//                    print(result.url)
//                    print(result.title)
                    let color = UITraitCollection.current.userInterfaceStyle == .dark ? "dark" : "light"
                    let url = "https://en.wikipedia.org/api/rest_v1/page/mobile-html/"+result.title+"?footer=true&theme="+color
                    let urlString = url.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)
//                    print(urlString!)
                    presenter.navToTest(url:urlString!)
                    
                }){
                    if(result.type=="wikipedia"){
                        HStack{
                            Text(AwesomeIcon.wikipediaW.rawValue)
                                .font(.awesome(style: .brand, size: 20))
                                .foregroundColor(.white)
                        Text(result.title)
                    }
                }
                    else if(result.type=="bookmark"){
                        HStack{
                            Image(systemName: "bookmark.fill").foregroundColor(Color.white)
                        Text(result.title)
                    }
                    }
                }
            }
        }
    }
}
