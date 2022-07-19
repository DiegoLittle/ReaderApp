//
//  BookmarksView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/21/22.
//

import Foundation
import SwiftUI

//struct BookmarksView: View {
//    var body: some View{
//        Text("Hello World")
//    }
//}
import SwiftUI
import Combine


//    Notification to listen for changes to the NoteList and reload
//func openSearch(){
//    presenter.navigationController!.navigationItem.titleView = UIHostingController(rootView: searchBarView().environmentObject(store)).view
//    presenter.navigationController!.navigationItem.hidesBackButton = true
//    presenter.navigationController!.navigationItem.leftBarButtonItem = UIBarButtonItem(
//        image: UIImage(systemName: "xmark")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
//        style: .plain,
//        target: self,
//        action: #selector(closeSearch))
//}
//@objc func closeSearch(){
//}
struct BookmarksView: View {
    @EnvironmentObject var store: AppStore
    @ObservedObject var viewModel = NoteListViewModel()
    @ObservedObject private var presenter: ContentPresenter
    
    var api = WebApi()
    
    
    init(presenter: ContentPresenter) {
        self.presenter = presenter
    }
    func deleteBookmark(at offsets: IndexSet){
        print(offsets)
        
        guard let index = Array(offsets).first else { return }
        print(index)
        print(store.state.bookmarks)
        
        print("Deleting the following index:")
        print(store.state.bookmarks[index])
        let bookmark = store.state.bookmarks[index]
        store.send(.deleteBookmark(bookmark))
//        API Request
        Task{
            do{
                try api.delete_bookmark(bookmark: bookmark)
            }
        }
    }
    
//    func loadResource(){
//
//    }
    
    func getSharedURLS(){
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//        test_url
        let syncing_bookmarks = sharedDefault.object(forKey: "syncing_bookmarks")as? NSArray ?? []
        print("syncing bookmarks:")
        print(syncing_bookmarks)
        if(syncing_bookmarks.count>0){
        for bookmark_data in syncing_bookmarks {
            do {
                // Create JSON Decoder
                let decoder = JSONDecoder()

                // Decode Note
                let bookmark = try decoder.decode(Bookmark.self, from: bookmark_data as! Data)
                store.send(.saveBookmark(bookmark))
                print(bookmark)
            } catch {
                print("Unable to Decode Note (\(error))")
            }
//            let bm_obj = Bookmark(
//                url:bookmark as! String, title:bookmark as! String)
        }
        sharedDefault.removeObject(forKey: "syncing_bookmarks")
        }

         
//        print(type(of: my_url!))
//        print(my_url!)
//        print(String(data:my_url! as! Data,encoding: .utf8))
    }


    var body: some View {

        VStack{
        NavigationView {
            List {
                ForEach(store.state.bookmarks){ bookmark in
//                    Button(action:{presenter.navToNote(noteViewModel: NoteViewModel(note))}){
//                        Text(note.title)
//                    }
                        Button(action:{
                            print(bookmark)
                            if(bookmark.type=="pdf"){
                                print("PDF")
                                print("Navigating to PDF")

                                presenter.navToPDF(path:bookmark.url!,bookmark:bookmark)
                            }
                            else if(bookmark.type=="arxiv_paper"){
                                var title_arr = bookmark.title!.split(separator: ".")
                                var file_ext = title_arr.removeLast()
                                let arxiv_id = title_arr.joined(separator: ".")
                                print("Navigating to arxiv vanity")
                                presenter.navToTest(url:"https://www.arxiv-vanity.com/papers/"+arxiv_id+"/")
                            }
//                            if(bookmark.type=="arxiv_papers"){
//                                print(bookmark.title!.split(separator: ".")[0])
////                                presenter.navToPDF(path:bookmark.url!)
////                                presenter.nav
//                            }
                            else{
                                print("Navigating to web page")
                                presenter.navToTest(url:bookmark.url!,bookmark:bookmark)
                            }
                            
                            
                            
                        }){
                            VStack(alignment:.leading,spacing: 1){

                            Text(bookmark.title ?? bookmark.url!)
                                .font(.title2)
                                .fontWeight(Font.Weight.semibold)
//                                .multilineTextAlignment(.leading)
//                                .frame(alignment:.leading)
                            if(bookmark.description != nil){
                                Text(bookmark.description!)
                                    .lineLimit(3)
                                    .font(.system(size:14))
//                                    .padding([.top],1)


                            }
                            }
                        }
                    
//                    NavigationLink(destination: NoteView(noteViewModel: NoteViewModel(note))
//                        ){
//                            Text(note.title)
//                        }
                }
                .onDelete(perform: deleteBookmark)
                .onAppear(perform:{
                    print("Fetching bookmarks")
                    Task{
                        try await api.get_bookmarks(store:store)
                    }
                })
            }
            .navigationBarTitle("Bookmarks")
            .navigationBarItems(trailing: Button(action:{presenter.navToTest(showSearch:true)}) {
                            Image(systemName: "magnifyingglass")
                                .resizable()
                                .padding(6)
                                .frame(width: 30, height: 30)
                                .background(Color.blue)
                                .clipShape(Circle())
                                .foregroundColor(.white)
                        }
            )
    
        }
        .onAppear {
            print("View Appeared!")
//                    FileManager.sharedContainerURL()
            let str = "Test Message"
            let url = FileManager.sharedContainerURL().appendingPathComponent("message.txt")
            let filepath = FileManager.sharedContainerURL().appendingPathComponent("test.txt").path
            print(filepath)
            do {
                try str.write(to: url, atomically: true, encoding: .utf8)
                let input = try String(contentsOf: url)
                print(input)
                FileManager.default.createFile(atPath:filepath,contents: input.data(using: .utf8))
            } catch {
                print("Error writting")
            }
            do {
                let dir = try FileManager.default.contentsOfDirectory(atPath:FileManager.sharedContainerURL().path)
                print(dir)
            } catch {
                print("Error reading directory")
            }
            
//                    presenter.navToPDF()
//                    var filemgr = FileManager.default
//                    var dir = filemgr.currentDirectoryPath
//                    do {
//                        try print(filemgr.contentsOfDirectory(atPath: "/"))
//                    } catch {
//                        print("Error reading directory")
//                    }
//                    let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//                    var pdf_path = sharedDefault.object(forKey: "pdf_path")
//                    print(pdf_path as! String)
//                    if let pdf = pdf_path {
//                        let filemgr = FileManager.default
//                        let databuffer = filemgr.contents(atPath: pdf as! String) ?? Data()
//                        print(databuffer)
////                        presenter.navToPDF(path:pdf as! String)
//                    }
//                    presenter.navToTest(url:bookmark.url!)}
//                    filemgr.contents(atPath: pdf_path)
//            print(store.state.bookmarks)
            self.viewModel.updateView()
//            print(self.viewModel.noteList)
            getSharedURLS()
            print("DEBUG")
//            print(store.state.searchResults)

            print(self.viewModel.theId)
            self.viewModel.getNotes()
            presenter.navigationController?.setNavigationBarHidden(true, animated: true)
            presenter.navigationController?.setToolbarHidden(true, animated: true)

        }
            
            
//            Custom bookmark list view but gonna halt on it because it might take more work than I expected. I'd have to implement the gesture for deleting and the styling is barely better
//            ForEach(store.state.bookmarks){ bookmark in
//                Button(action:{
//                    print(bookmark)
//                    if(bookmark.type=="pdf"){
//                        print("PDF")
//                        presenter.navToPDF(path:bookmark.url!)
//                    }
//                    else{
//                        presenter.navToTest(url:bookmark.url!)
//                    }
//
//
//
//                }){
//                    BookmarkListCell(
//                        title:bookmark.title!,
//                        description:bookmark.description ?? ""
//                    )
//                }
//            }
    }
    }

}


//struct BookmarkListCell:View{
//    var title:String
//    var description:String
//    var body:some View{
//        HStack{
//            Color(red: 68 / 255, green: 68 / 255, blue: 68 / 255)
//                .overlay(
//                    VStack(alignment:.leading) {
//                        Text(title)
//                            .font(.title2)
//                            .fontWeight(Font.Weight.semibold)
//                            .frame(alignment:.leading)
//                            .foregroundColor(Color.white)
//                        Text(description)
//                            .lineLimit(3)
//                            .font(.system(size:14))
//                            .frame(alignment:.leading)
//                            .foregroundColor(Color.white)
//                }
//                        .padding([.horizontal])
//                )
////            Spacer()
//        }.cornerRadius(10)
//            .frame(maxHeight:100)
//
//    }
//}
