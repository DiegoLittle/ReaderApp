//
//  NoteListView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/20/22.
//

//
//  EntryListView.swift
//  Journal
//
//  Created by Diego Little on 10/16/21.
//

import SwiftUI
import Combine

class MyTimer {
    let currentTimePublisher = Timer.TimerPublisher(interval: 1.0, runLoop: .main, mode: .default)
    let cancellable: AnyCancellable?

    init() {
        self.cancellable = currentTimePublisher.connect() as? AnyCancellable
    }

    deinit {
        self.cancellable?.cancel()
    }
}

let timer = MyTimer()

var webapi = WebApi()


struct NoteListView: View {
    @ObservedObject var viewModel = NoteListViewModel()
    @State var refresh: Bool = false
    @State private var theId = 0
    @State private var currentTime: Date = Date()
    @ObservedObject private var presenter: ContentPresenter

    init(presenter: ContentPresenter) {
        self.presenter = presenter
    }
//    Notification to listen for changes to the NoteList and reload
    
    var body: some View {
//        VStack{
        NavigationView {
            List {
                ForEach(self.viewModel.noteList){ note in
                    Button(action:{
                        presenter.navToNote(noteViewModel: NoteViewModel(note))
                        
                    }){
                        Text(note.title)
                    }
//                    NavigationLink(destination: NoteView(noteViewModel: NoteViewModel(note))
//                        ){
//                            Text(note.title)
//                        }
                }
                .onDelete(perform: self.viewModel.deleteNote)
                .onAppear(perform:{
                    
                    self.viewModel.updateView()
                    print(self.viewModel.noteList)
                })
            }
//            .navigationBarTitle("Notes")
            .navigationBarItems(trailing: Button(action:{presenter.navToNote(noteViewModel: NoteViewModel())}) {
                            Image(systemName: "plus")
                                .resizable()
                                .padding(6)
                                .frame(width: 24, height: 24)
                                .background(Color.blue)
                                .clipShape(Circle())
                                .foregroundColor(.white)
                        }
            )
    
        }
        .onAppear {
            print("DEBUG")
            print(self.viewModel.theId)
            self.viewModel.getNotes()
        }
        .onDisappear {
            print("DEBUG")
            
            self.viewModel.getNotes()
        }
        .onReceive(timer.currentTimePublisher){ newCurrentTime in
//            self.theId += 1
            self.currentTime = newCurrentTime
        }
//    }
    }

}
