//
//  SearchView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/22/22.
//

import Foundation
//
//  ContentView.swift
//  GithubSearch
//
//  Created by Majid Jabrayilov on 6/4/19.
//  Copyright © 2019 Majid Jabrayilov. All rights reserved.
//
import SwiftUI
import Combine

struct RepoRow: View {
    let repo: Repo

    var body: some View {
        HStack(alignment: .top) {
            VStack(alignment: .leading) {
                Text(repo.name)
                    .font(.headline)
                Text(repo.description ?? "")
                    .font(.subheadline)
            }
        }
    }
}

struct SearchContainerView: View {
    @EnvironmentObject var store: AppStore
    @State private var query: String = "Swift"

    var body: some View {
        SearchView(
            query: $query,
            repos: store.state.GithubSearchResult,
            onCommit: fetch
        ).onAppear(perform: fetch)
    }

    private func fetch() {
//        store.send(.search(query: query))
    }
}

struct SearchView : View {

    @Binding var query: String
    let repos: [Repo]
    let onCommit: () -> Void

    var body: some View {
        let binding = Binding<String>(get: {
            self.query
        }, set: {

            if(self.query != $0){
                self.query = $0
                onCommit()
            }
            
            // do whatever you want here
        })
        NavigationView {
            List {
                TextField("Type something", text: binding)

                if repos.isEmpty {
                    Text("Loading...")
                } else {
                    ForEach(repos) { repo in
                        RepoRow(repo: repo)
                    }
                }
            }.navigationBarTitle(Text("Search"))
        }
    }
}
