//
//  SearchService.swift
//  ReaderApp
//
//  Created by Diego Little on 4/22/22.
//

import Foundation
//
//  GithubService.swift
//  ReaderApp
//
//  Created by Diego Little on 4/22/22.
//


import SwiftUI
import Combine
import Fuse
import StringMetric
import NaturalLanguage
import SwiftAnnoy
//
//struct Repo: Decodable, Identifiable {
//    var id: Int
//    let owner: Owner
//    let name: String
//    let description: String?
//
//    struct Owner: Decodable {
//        let avatar: URL
//
//        enum CodingKeys: String, CodingKey {
//            case avatar = "avatar_url"
//        }
//    }
//}


//struct SearchResponse: Decodable {
//    let items: [Repo]
//}
struct SearchResult: Identifiable,Codable{
var id: UUID = UUID()
var url:String
var title:String
    var type:String?
}
enum SearchAPIError: Error, LocalizedError {
    case unknown, apiError(reason: String)

    var errorDescription: String? {
        switch self {
        case .unknown:
            return "Unknown error"
        case .apiError(let reason):
            return reason
        }
    }
}

class SearchService {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared, decoder: JSONDecoder = .init()) {
        self.session = session
        self.decoder = decoder
    }
    enum HTTPError: LocalizedError {
        case statusCode
    }
    func fetch(url: URL) -> AnyPublisher<Data, SearchAPIError> {
        let request = URLRequest(url: url)
        print("Fetch function in Search Service")

        return URLSession.DataTaskPublisher(request: request, session: .shared)
            .tryMap { data, response in
                print(response)
                print(data)
                guard let httpResponse = response as? HTTPURLResponse, 200..<300 ~= httpResponse.statusCode else {
                    throw SearchAPIError.unknown
                }
                return data
            }
            .mapError { error in
                if let error = error as? SearchAPIError {
                    return error
                } else {
                    return SearchAPIError.apiError(reason: error.localizedDescription)
                }
            }
            .eraseToAnyPublisher()
    }
    
    
    
    
    func searchPublisher(query: String, completionHandler: @escaping ([SearchResult]) -> ([SearchResult])){
     
        guard var urlComponents = URLComponents(string: "https://en.wikipedia.org/w/api.php")else {
            print("Can't create url components...")
            preconditionFailure("Can't create url components...") }
        urlComponents.queryItems = [
            URLQueryItem(name:"action",value:"opensearch"),
            URLQueryItem(name: "search", value: query)
        ]
        guard
            let url = urlComponents.url
            else {
            print("Can't create url components...")
            preconditionFailure("Can't create url from url components...") }
        var SearchResults: [SearchResult] = []
        URLSession.shared.dataTask(with: url) { data, response, error in
            print(data)
            if let error = error {
                print(error)
                return
            }
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                print(response)
                return
            }
            var mimeType = httpResponse.mimeType
            if(mimeType == "application/json"){
               let data = data
                var json = try? JSONSerialization.jsonObject(with: data!, options: JSONSerialization.ReadingOptions()) as? [Any]
                print(type(of: json![1]))

                var i:Int = 0
                for value in json![1] as! NSArray{
                    let urls = json![3] as! NSArray
                    let item = SearchResult(url:urls[i] as! String, title:value as! String,type:"wikipedia")
                        SearchResults.append(item)
                    i+=1
                  }
                completionHandler(SearchResults)
            }
            completionHandler(SearchResults)
        }.resume()
    }
    
    func write_bookmark_embeddings(bookmarks:[Bookmark]) throws {
        var dictionary = Dictionary<UUID, Array<Double>>()
        for bookmark in bookmarks{
            if let sentenceEmbedding = NLEmbedding.sentenceEmbedding(for: .english) {


                if let vector = sentenceEmbedding.vector(for: bookmark.title ?? "") {
                    dictionary[bookmark.id] = vector
                    let url = FileManager.sharedContainerURL().appendingPathComponent("vectors.json")
                    let encoder = JSONEncoder()
                    if let jsonData = try? encoder.encode(dictionary) {
                        if let jsonString = String(data: jsonData, encoding: .utf8) {
                            try jsonString.write(to: url, atomically: true,encoding: String.Encoding.utf8)
//                            NSDictionary(dictionary: dictionary).write(to: url, atomically: true)

                            
                            
//                            NSDictionary(dictionary: dictionary).write(to: url, atomically: true)
//                            let customDict = NSDictionary(contentsOf: url)
//                            print(customDict)
//                            let customDict = NSDictionary(contentsOf: url)
//                            print(customDict)
                        }
                    }
                }

//                let distance = sentenceEmbedding.distance(between: sentence, and: "That is a sentence.")
//                print(distance.description)
            }
        }
        
    }
    
    func test(query: String,store: AppStore) async throws -> [SearchResult]{
//        store.state.bookmarks
//        let fuse = Fuse()
        struct Item {
        let label:String
            let score:Double
        }
//        let results = fuse.search("Simple", in: store.state.bookmarks)
//        var bookmark_titles:Array<String> = []
//        for bookmark in store.state.bookmarks{
//            bookmark_titles.append(bookmark.title!)
//        }
//        let read_json = try String(contentsOf:url,encoding:.utf8)
//        print(read_json)
//        let decoded = try JSONDecoder().decode([UUID: Array<Double>].self, from: jsonData)
        let url = FileManager.sharedContainerURL().appendingPathComponent("vectors.json")

        let read_json = try String(contentsOf:url,encoding:.utf8)
//                            print(read_json)
        let decoded = try JSONDecoder().decode([UUID: Array<Double>].self, from: read_json.data(using: .utf8) ?? Data())
        
        
        
        
//        If number of bookmarks is different than embeddings dictionary key
//        Then recompute bookmark embeddings
//        if(decoded.keys.count != store.state.bookmarks.count){
//            try write_bookmark_embeddings(bookmarks: store.state.bookmarks)
//        }
//        var index = AnnoyIndex<Double>(itemLength: 512, metric: .euclidean)
//
//        var items = Array(decoded.values)
//
//        try? index.addItems(items: &items)
//
//        try? index.build(numTrees: 8)
//        if let sentenceEmbedding = NLEmbedding.sentenceEmbedding(for: .english) {
//            let sentence = query
//
//            if var vector = sentenceEmbedding.vector(for: sentence) {
//                let results2 = index.getNNsForVector(vector: &vector, neighbors: 3)
//                for ind in results2!.indices{
//                    print(store.state.bookmarks[ind].title)
//                }
//            }
//        }

        
        
        
        // Improve performance by creating the pattern once
//        let pattern = fuse.createPattern(from: query)
//        print(bookmark_titles)
        var SearchResults: [SearchResult] = []
        // Search for the pattern in every book
        
        
        
        
//        let url = FileManager.sharedContainerURL().appendingPathComponent("embeddings.plist")
//        NSDictionary(dictionary: dictionary).write(to: url, atomically: true)
//

//        bookmark_titles.forEach{

////            let result = fuse.search(pattern, in: $0)
////            print(query.distance(between: $0))
//////            print(result?.score)
//////            print(result?.ranges)
////            print($0)
//        }
//        store.state.bookmarks.forEach {
//            let result = fuse.search(pattern, in: $0.title!)
////            print(result?.score)
////            print(result?.ranges)
////            print($0)
//            if (result?.score != nil){
//                print(result?.score)
//                print($0.title)
//                let search_result = SearchResult(
//                    url:$0.url!,
//                    title:$0.title!, type: "bookmark"
//                )
//                SearchResults.append(search_result)
//            }
//        }
//        sort items by score
//        items.sort { $0.score > $1.score }
//        print(items)
//        let results = fuse.search(query, in: store.state.bookmarks)
        
////        print(results)
//        results.forEach { item in
//            print("index: " + String(item.index))
//            print("score: " + String(item.score))
//            print(item.results)
//            print("---------------")
//        }
        guard var urlComponents = URLComponents(string: "https://en.wikipedia.org/w/api.php")else {
            print("Can't create url components...")
            preconditionFailure("Can't create url components...") }
        urlComponents.queryItems = [
            URLQueryItem(name:"action",value:"opensearch"),
            URLQueryItem(name: "search", value: query)
        ]
        guard
            let url = urlComponents.url
            else {
            print("Can't create url components...")
            preconditionFailure("Can't create url from url components...") }
        let (data,response) = try await URLSession.shared.data(from: url)
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                
//                print(response)
                throw HTTPError.statusCode
            }
            var mimeType = httpResponse.mimeType
            if(mimeType == "application/json"){
               let data = data
                var json = try? JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions()) as? [Any]
                print(type(of: json![1]))

                var i:Int = 0
                for value in json![1] as! NSArray{
                    let urls = json![3] as! NSArray
                    let item = SearchResult(url:urls[i] as! String, title:value as! String,type:"wikipedia")
                        SearchResults.append(item)
                    i+=1
                  }
            }
        return SearchResults
    }
    
    
}
