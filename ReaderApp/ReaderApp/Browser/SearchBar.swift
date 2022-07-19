//
//  SearchBar.swift
//  ReaderApp
//
//  Created by Diego Little on 4/30/22.
//

import Foundation
import SwiftUI
import WebKit
import FontAwesomeSwiftUI

struct searchBarView: View {

    @State var query: String = ""
    @FocusState private var isFocused:Bool
    @EnvironmentObject var store: AppStore
    @State var search_mode:String = "web"
    @ObservedObject var presenter: ContentPresenter

    private func fetch() {
//        if (self.search_mode=="wikipedia") {
            Task{
                let results = try await searchService.test(query:query,store:store)
                store.send(.setSearchResults(results: results))
            }
//        }
        print("Fetching results")
        
    }
    var body: some View{
        let binding = Binding<String>(get: {
            self.query
        }, set: {
            if(self.query != $0){
                self.query = $0
                print("Query changes")
                print($0)
                fetch()
            }
            
            // do whatever you want here
        })
        HStack{
            TextField("",text:binding,onCommit: {
                if(search_mode=="web" && self.query != ""){
                print("Google searching")
                    let query_string = self.query.replacingOccurrences(of: " ", with: "%20")
                let webURL = "https://www.google.com/search?q="+query_string
                   
        
                    print(webURL)
                presenter.navToTest(url:webURL)
                }
//                Navigate to webview with the url of https://www.google.com/search?q=query
            })
                .introspectTextField { uiTextField in
                    uiTextField.becomeFirstResponder()
                    uiTextField.attributedPlaceholder = NSAttributedString(string: "search",
                    attributes: [NSAttributedString.Key.foregroundColor: UIColor.gray]
                
                    )
                }
                .foregroundColor(Color.white)
            Button(action:{
                if(self.search_mode=="wikipedia"){
                    self.search_mode = "web"
                }
                else{
                    self.search_mode = "wikipedia"
                }
            }){
                Text(AwesomeIcon.google.rawValue)
                    .font(.awesome(style: .brand, size: 20))
                    .foregroundColor(iconColor(search_mode: self.search_mode))
            }
            Button(action:{
                self.query=""
            }){
                Image(systemName: "xmark")
            }

//            ZStack{
//                Circle().fill(Color(red: 211 / 255, green: 211 / 255, blue: 211 / 255)).padding(2)
//            }
//            .frame(alignment: .trailing)

        }
        .frame(height: 30)
        .padding([.vertical],5)
        .padding([.horizontal],10)
        .background(
            RoundedRectangle(cornerRadius: 10,style: .continuous)
                .fill(Color(red: 68 / 255, green: 68 / 255, blue: 68 / 255))
        )
    }
}


func iconColor(search_mode:String) -> Color{
    
    if(search_mode=="wikipedia"){
        return Color.blue
    }
    else{
        return Color.white
    }
    
}
