//
//  ContentView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/20/22.
//

//
//  ContentView.swift
//  SwiftUI Router
//
//  Created by Phil Yates on 12/02/2021.
//

import SwiftUI
import UIKit

final class ContentPresenter:
    ObservableObject {
    var store:AppStore
    
    init(store:AppStore){
        self.store = store
        
    }

    weak var navigationController: UINavigationController?
    
    func navToNote(noteViewModel: NoteViewModel){
        
        let vc = UIHostingController(rootView: NoteView(noteViewModel:noteViewModel))
        navigationController?.pushViewController(vc, animated: true)
    }
    func navToTest(url:String? = nil,showSearch:Bool = false,bookmark:Bookmark? = nil){
        self.navigationController?.setNavigationBarHidden(false, animated: true)
        self.navigationController?.setToolbarHidden(false, animated: true)
        var vc:Browser
        if(bookmark != nil){
        vc = Browser(
            presenter:self,
            url:url,
            store:store,
            showSearch:showSearch,
            bookmark:bookmark!
        )
        }
        else{
            vc = Browser(
                presenter:self,
                url:url,
                store:store,
                showSearch:showSearch
            )
        }
//        let searchBar = UISearchBar()
//        searchBar.sizeToFit()
//        navigationController?.navigationItem.titleView = searchBar
//        self.navigationController?.interactivePopGestureRecognizer?.isEnabled = false
//        navigationController?.searchDisplayController?.displaysSearchBarInNavigationBar = true

        navigationController?.pushViewController(vc, animated: true)
        
    }
    func navToPDF(path:String = "",bookmark:Bookmark = Bookmark()){
        self.navigationController?.setNavigationBarHidden(false, animated: true)
        self.navigationController?.setToolbarHidden(false, animated: true)
        let vc = PDFViewController(
            presenter:self,
            store:store,
            path:path,
            bookmark:bookmark)
//        let searchBar = UISearchBar()
//        searchBar.sizeToFit()
//        navigationController?.navigationItem.titleView = searchBar
//        self.navigationController?.interactivePopGestureRecognizer?.isEnabled = false
//        navigationController?.searchDisplayController?.displaysSearchBarInNavigationBar = true

        navigationController?.pushViewController(vc, animated: true)
    }
    func navToArticle(){
        
        let vc = UIHostingController(rootView: HomeView())
        navigationController?.pushViewController(vc, animated: true)
    }
}

struct ContentView: View {
    @Environment(\.window) var window: UIWindow?
    @ObservedObject private var presenter: ContentPresenter
    
    init(presenter: ContentPresenter) {
        self.presenter = presenter
    }
    
    var body: some View {
                TabView{
                    BookmarksView(presenter: self.presenter)
                        .tabItem{
                            Image(systemName: "bookmark.fill")
                        }
                    NoteListView(presenter:self.presenter)
                        .tabItem{
                            Image(systemName: "note.text")
                        }
                    SignInView()
                        .tabItem{
                            Image(systemName: "note.text")
                        }
//                    SearchContainerView()
//                        .tabItem{
//                            Image(systemName: "newspaper.fill")
//                        }

                }
//        Button(action: { presenter.buttonTapped() }) {
//            Text("Navigate")
//        }
    }
}

//struct ContentView_Previews: PreviewProvider {
//    static var previews: some View {
//        ContentView(presenter: ContentPresenter())
//    }
//}
