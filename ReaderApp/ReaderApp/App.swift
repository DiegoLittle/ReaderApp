//
//  App.swift
//  ReaderApp
//
//  Created by Diego Little on 4/22/22.
//

import Foundation
//
//  App.swift
//  GithubSearch
//
//  Created by Majid Jabrayilov on 9/16/19.
//  Copyright © 2019 Majid Jabrayilov. All rights reserved.
//
import Combine
import RealmSwift

// For more information check "How To Control The World" - Stephen Celis
// https://vimeo.com/291588126
struct World {
    var github_service = GithubService()
    var service = SearchService()
}

enum AppAction {
    case setGithubSearchResults(repos: [Repo])
    case setSearchResults(results: [SearchResult])
    case searchGithub(query: String)
    case search(query: String)
    case saveBookmark(Bookmark)
    case deleteBookmark(Bookmark)
    case updateBookmark(Bookmark)
}

struct AppState: Codable {
    var _id: ObjectId = ObjectId()
    var GithubSearchResult: [Repo] = []
    var bookmarks: [Bookmark] = []
    var searchResults: [SearchResult] = []
    init(){
        let realm = try! Realm()
        let results = realm.objects(AppStateObject.self).toArray()
        print("Initalizing app state")
        print(results)
        if(results.count > 0){
            let state = results[0].state
            self._id = results[0]._id
            self.searchResults = state.searchResults
            self.GithubSearchResult = state.GithubSearchResult
            self.bookmarks = state.bookmarks
            self.searchResults = state.searchResults
        }

    }
}
class AppStateObject : Object {
    @Persisted(primaryKey: true) var _id: ObjectId
    @Persisted private dynamic var structData:Data? = nil
//    @Persisted var test = "Hello World"
    
//    func setState(myStruct:AppState){
//        self.structData = try? JSONEncoder().encode(myStruct)
//    }

    var state : AppState {
        get {
            return try! JSONDecoder().decode(AppState.self, from: structData!)
        }
        set {
            structData = try! JSONEncoder().encode(newValue)
        }
    }
}

func appReducer(
    state: inout AppState,
    action: AppAction,
    environment: World
) -> AnyPublisher<AppAction, Never> {
    switch action {
    case let .saveBookmark(bookmark):
        
        state.bookmarks.insert(bookmark,at:0)
//        state.bookmarks.append(bookmark)
    case let .deleteBookmark(bookmark):
        print(state.bookmarks)
//        if let index = animals.firstIndex(of: "chimps") {
//            animals.remove(at: index)
//        }
//        print("Saving store to realm")
        state.bookmarks = state.bookmarks.filter { $0 != bookmark }
//        state.bookmarks.remove(at: <#T##Int#>)
    case let .setSearchResults(results):
        state.searchResults = results
    case let .setGithubSearchResults(repos):
        state.GithubSearchResult = repos
    case let .updateBookmark(bookmark):
        for (i,x) in state.bookmarks.enumerated(){
            if(x.id == bookmark.id){
                print(bookmark)
//                print(x)
                state.bookmarks[i] = bookmark
            }
//            print(x)
//            print(bookmark)
//            print(i)
//            print(x)
//            print()
        }
        
    case let .searchGithub(query):
        print(query)
        return environment.github_service
            .searchPublisher(matching: query)
            .catch { error -> AnyPublisher<[Repo], Never> in
                print(error)
                return Just([])
                    .eraseToAnyPublisher()
                        }
            .replaceError(with: [])
            .map {
                print($0)
                return AppAction.setGithubSearchResults(repos: $0) }
            .eraseToAnyPublisher()
    case let .search(query):
//        print(query)
        var results:[SearchResult]=[]
        let semaphore = DispatchSemaphore(value: 0)
        environment.service.searchPublisher(query: query){ (result) in
            semaphore.signal()
            results = result
            return result
        }

        semaphore.wait()
        state.searchResults = results
//            .map{
//
//            }
    }
//    Save store to realm
    print("Saving store to realm")
//    print(state)
    let realm = try! Realm()
    try! realm.write {
        let myReal = AppStateObject()
        myReal._id = state._id
        myReal.state = state
//        print(myReal)
        realm.add(myReal,update: .all)
    }
//    let container = try! Container()
//    try! container.write { transaction in
//        transaction.add(state, update: true)
//    }
    
//    Get App States and delete them
//    let realm = try! Realm()
    var results = realm.objects(AppStateObject.self).toArray()
//    print(results)
//    for result in results{
//        let obj = realm.object(ofType: AppStateObject.self, forPrimaryKey: result._id)!
//        if(obj.isInvalidated==false){
//            try! realm.write {
//                 realm.delete(obj)
//             }
//        }
//    }
////    results = realm.objects(AppStateObject.self).toArray()
//    print(results)
    return Empty().eraseToAnyPublisher()
}

typealias AppStore = Store<AppState, AppAction, World>

