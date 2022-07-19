//
//  GithubService.swift
//  ReaderApp
//
//  Created by Diego Little on 4/22/22.
//

import Foundation
//
//  File.swift
//  GithubSearch
//
//  Created by Majid Jabrayilov on 6/5/19.
//  Copyright © 2019 Majid Jabrayilov. All rights reserved.
//

import SwiftUI
import Combine
import RealmSwift

struct Repo: Codable, Identifiable{
    var id: Int
    let owner: Owner
    let name: String
    let description: String?

    struct Owner: Codable {
        let avatar: URL

        enum CodingKeys: String, CodingKey {
            case avatar = "avatar_url"
        }
    }
}


struct SearchResponse: Decodable {
    let items: [Repo]
}

class GithubService {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared, decoder: JSONDecoder = .init()) {
        self.session = session
        self.decoder = decoder
    }

    func searchPublisher(matching query: String) -> AnyPublisher<[Repo], Error> {
        guard
            var urlComponents = URLComponents(string: "https://api.github.com/search/repositories")
            else {
            print("Can't create url components...")
            preconditionFailure("Can't create url components...") }

        urlComponents.queryItems = [
            URLQueryItem(name: "q", value: query)
        ]

        guard
            let url = urlComponents.url
            else {
            print("Can't create url components...")
            preconditionFailure("Can't create url from url components...") }
            
        return session
            .dataTaskPublisher(for: url)
            .map {
                print(String(data: $0.data, encoding:. utf8))
                return $0.data }
            .decode(type: SearchResponse.self, decoder: decoder)
            .map { $0.items }
            .eraseToAnyPublisher()
    }
}
