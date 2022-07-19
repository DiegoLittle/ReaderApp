/// Copyright (c) 2019 Razeware LLC
/// 
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
/// 
/// The above copyright notice and this permission notice shall be included in
/// all copies or substantial portions of the Software.
/// 
/// Notwithstanding the foregoing, you may not use, copy, modify, merge, publish,
/// distribute, sublicense, create a derivative work, and/or sell copies of the
/// Software in any work that is designed, intended, or marketed for pedagogical or
/// instructional purposes related to programming, coding, application development,
/// or information technology.  Permission for such use, copying, modification,
/// merger, publication, distribution, sublicensing, creation of derivative works,
/// or sale is expressly withheld.
/// 
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
/// THE SOFTWARE.

import Foundation
//let remote_url = ProcessInfo.processInfo.environment["reader_app_remote"]
//let remote_url = "http://165.232.156.229:8000"
let remote_url = Bundle.main.object(forInfoDictionaryKey: "WEBSERVICE_URL") as! String

enum WebApiError: Error, LocalizedError {
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

struct WebApi {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared, decoder: JSONDecoder = .init()) {
        self.session = session
        self.decoder = decoder
    }
    enum HTTPError: LocalizedError {
        case statusCode
    }
    func update_bookmark(bookmark:Bookmark) throws -> Bool{
        var url = URL(string:remote_url+"/bookmark")
        var request = URLRequest(
            url: url!,
            cachePolicy: .reloadIgnoringLocalCacheData
        )
        var jsonData:Data
//        var dummy = DummyData(email: "diegochelittle@gmail.com", name: "Diego Little", identifier: "jlkfdiasudhfiausdghar;lk")
        jsonData = try JSONEncoder().encode(bookmark)
        let jsonString = String(data: jsonData, encoding: .utf8)!
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//        var body = "Hello World".data(using: .utf8)
        let refresh_token_object = sharedDefault.object(forKey: "refresh_token") as? String
        let user_id_object = sharedDefault.object(forKey: "user_id" ) as? String
        if(refresh_token_object == nil){
            print("Refresh_token is nil")
            return false
        }
        if(user_id_object == nil){
            print("User id is nil")
            return false
        }
        struct RequestBody: Codable {
        let bookmark: Bookmark
        let refresh_token: String
        let user_id: String
        }
        print(bookmark)
        var request_body = RequestBody(
            bookmark:bookmark,
            refresh_token: refresh_token_object!,
            user_id: user_id_object!
        )
        print(request_body)
        let body = try JSONEncoder().encode(request_body)
//        let body = jsonData
        
//        let body = try JSONEncoder().encode(my_dict)
        request.httpMethod = "PUT"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(
            with: request,
            completionHandler: { data, response, error in
                // Validate response and call handler
                print(String(decoding:data ?? Data(), as: UTF8.self))
            }
        )
        task.resume()
        return true
    }
    func delete_bookmark(bookmark:Bookmark) throws -> Bool{
        var url = URL(string:remote_url+"/bookmark")
        var request = URLRequest(
            url: url!,
            cachePolicy: .reloadIgnoringLocalCacheData
        )
        var test = "Hello World"
        var jsonData:Data
//        var dummy = DummyData(email: "diegochelittle@gmail.com", name: "Diego Little", identifier: "jlkfdiasudhfiausdghar;lk")
        jsonData = try JSONEncoder().encode(bookmark)
        let jsonString = String(data: jsonData, encoding: .utf8)!
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//        var body = "Hello World".data(using: .utf8)
        let refresh_token_object = sharedDefault.object(forKey: "refresh_token") as? String
        let user_id_object = sharedDefault.object(forKey: "user_id" ) as? String
        if(refresh_token_object == nil){
            print("Refresh_token is nil")
            return false
        }
        if(user_id_object == nil){
            print("User id is nil")
            return false
        }
        struct RequestBody: Codable {
        let bookmark: Bookmark
        let refresh_token: String
        let user_id: String
        }
        print(bookmark)
//        if (bookmark.description == nil) {
////            bookmark.description = ""
//        }
        
        let body = try JSONEncoder().encode(RequestBody(bookmark:bookmark,refresh_token: refresh_token_object!,user_id: user_id_object!))
//        let body = jsonData
        
//        let body = try JSONEncoder().encode(my_dict)
        request.httpMethod = "DELETE"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(
            with: request,
            completionHandler: { data, response, error in
                // Validate response and call handler
                print(String(decoding:data ?? Data(), as: UTF8.self))
            }
        )
        task.resume()
        return true
    }
    func post_bookmark(bookmark:Bookmark) throws -> Bool{
        var url = URL(string:remote_url+"/bookmark")
        var request = URLRequest(
            url: url!,
            cachePolicy: .reloadIgnoringLocalCacheData
        )
        var test = "Hello World"
        var jsonData:Data
//        var dummy = DummyData(email: "diegochelittle@gmail.com", name: "Diego Little", identifier: "jlkfdiasudhfiausdghar;lk")
        jsonData = try JSONEncoder().encode(bookmark)
        let jsonString = String(data: jsonData, encoding: .utf8)!
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//        var body = "Hello World".data(using: .utf8)
        let refresh_token_object = sharedDefault.object(forKey: "refresh_token") as? String
        let user_id_object = sharedDefault.object(forKey: "user_id" ) as? String
        if(refresh_token_object == nil){
            print("Refresh_token is nil")
            return false
        }
        if(user_id_object == nil){
            print("User id is nil")
            return false
        }
        struct RequestBody: Codable {
        let bookmark: Bookmark
        let refresh_token: String
        let user_id: String
        }
        let body = try JSONEncoder().encode(RequestBody(bookmark:bookmark,refresh_token: refresh_token_object!,user_id: user_id_object!))
//        let body = jsonData
        
//        let body = try JSONEncoder().encode(my_dict)
        request.httpMethod = "POST"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(
            with: request,
            completionHandler: { data, response, error in
                // Validate response and call handler
                print(String(decoding:data ?? Data(), as: UTF8.self))
            }
        )
        task.resume()
        return true
    }
    func get_bookmarks(store: AppStore) async throws -> Bool{
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
        let refresh_token_object = sharedDefault.object(forKey: "refresh_token") as? String
        let user_id_object = sharedDefault.object(forKey: "user_id" ) as? String
        if(refresh_token_object == nil){
            print("Refresh_token is nil")
            return false
        }
        if(user_id_object == nil){
            print("User id is nil")
            return false
        }
//        var url = URL(string:)
        var url = URLComponents(string: remote_url+"/bookmarks")!
        url.queryItems = [
            URLQueryItem(name: "refresh_token", value: refresh_token_object),
            URLQueryItem(name:"user_id",value:user_id_object)
        ]
//        var body = "Hello World".data(using: .utf8)

//        guard var urlComponents = URLComponents(string: url)else {
//            print("Can't create url components...")
//            preconditionFailure("Can't create url components...") }
//        urlComponents.queryItems = [
//            URLQueryItem(name:"action",value:"opensearch"),
//            URLQueryItem(name: "search", value: query)
//        ]
//        guard
//            let url = urlComponents.url
//            else {
//            print("Can't create url components...")
//            preconditionFailure("Can't create url from url components...") }
//        var SearchResults: [SearchResult] = []
        struct bookmark_res{
            var description:String
            var id:String
            var owner_id: String
            var title:String
            var type:String
            var url:String
        }
        let (data,response) = try await URLSession.shared.data(from: url.url!)
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                
                print(response)
                throw HTTPError.statusCode
            }
            var mimeType = httpResponse.mimeType
            if(mimeType == "application/json"){
               let data = data
                var json = try? JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions()) as? [Any]
                print(json)
                if let bookmarks = json{
                    print(bookmarks)
                    for x in bookmarks{
//                        print(x as! bookmark_res)
                        var res = x as! NSDictionary
//                        for (key, value) in x as! NSDictionary {
//                            print("Value: \(value) for key: \(key)")
//                        }
                        var description:String?
                        if(res["description"] as? String == "<null>"){
                            description = ""
                        }
                        else{
                            description = res["description"] as? String
                        }
                        let bookmark = Bookmark(
                            id:UUID(uuidString: res["id"] as! String)!,
                            url:res["url"] as? String,
                            title:res["title"] as? String,
                            description: description
                        )
                        if store.state.bookmarks.contains(bookmark){
                            print("Bookmark already in state")
                        }
                        else{
                          store.send(.saveBookmark(bookmark))
                        }
                    }
                }
            }
        return true
    }
    func get() async throws -> Void{
        var url = "https://localhost:8000/"
        guard var urlComponents = URLComponents(string: url)else {
            print("Can't create url components...")
            preconditionFailure("Can't create url components...") }
//        urlComponents.queryItems = [
//            URLQueryItem(name:"action",value:"opensearch"),
//            URLQueryItem(name: "search", value: query)
//        ]
        guard
            let url = urlComponents.url
            else {
            print("Can't create url components...")
            preconditionFailure("Can't create url from url components...") }
//        var SearchResults: [SearchResult] = []
        let (data,response) = try await URLSession.shared.data(from: url)
            guard let httpResponse = response as? HTTPURLResponse,
                (200...299).contains(httpResponse.statusCode) else {
                
                print(response)
                throw HTTPError.statusCode
            }
            var mimeType = httpResponse.mimeType
            if(mimeType == "application/json"){
               let data = data
                var json = try? JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions()) as? [Any]
                print(json)
            }
    }
    
    struct DummyData: Codable {
      /// The email address to use for user communications.  Remember it might be a relay!
      let email: String

      /// The components which make up the user's name.  See `displayName(style:)`
      let name: String

      /// The team scoped identifier Apple provided to represent this user.
      let identifier: String
    }
    
    func post() async throws -> Void{
        var url = URL(string:remote_url+"/test")
        var request = URLRequest(
            url: url!,
            cachePolicy: .reloadIgnoringLocalCacheData
        )
        var test = "Hello World"
        var jsonData:Data
        var dummy = DummyData(email: "diegochelittle@gmail.com", name: "Diego Little", identifier: "jlkfdiasudhfiausdghar;lk")
        jsonData = try JSONEncoder().encode(dummy)
        let jsonString = String(data: jsonData, encoding: .utf8)!
//        var body = "Hello World".data(using: .utf8)
        struct RequestBody: Encodable {
        let user: DummyData
        let identityToken: String
        }
        let body = try JSONEncoder().encode(RequestBody(user: dummy, identityToken: "Hello World"))
//        let body = jsonData
        
//        let body = try JSONEncoder().encode(my_dict)
        request.httpMethod = "POST"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(
            with: request,
            completionHandler: { data, response, error in
                // Validate response and call handler
                print(String(decoding:data ?? Data(), as: UTF8.self))
//                print(response)
            }
        )
        task.resume()
    }
    static func SignIn(user_id:String, identityToken:String, authorizationCode:String) throws -> Bool{

        var url = URL(string:remote_url+"/apple_login")
        var request = URLRequest(
            url: url!,
            cachePolicy: .reloadIgnoringLocalCacheData
        )
        struct RequestBody: Encodable {
        let user_id: String
        let identityToken: String
        let authorizationCode:String
        }
        let body = try JSONEncoder().encode(RequestBody(user_id: user_id, identityToken: identityToken, authorizationCode: authorizationCode))
//        let body = jsonData

//        let body = try JSONEncoder().encode(my_dict)
        request.httpMethod = "POST"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(
            with: request,
            completionHandler: { data, response, error in
                // Validate response and call handler
                let decoder = JSONDecoder()
                do {
                    let token_response = try decoder.decode(token_response.self, from: data!)
//                    print(token_response.refresh_token)
                    let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
                    sharedDefault.set(token_response.refresh_token, forKey: "refresh_token" )
                    sharedDefault.set(user_id, forKey: "user_id" )
                } catch {
                    print(error.localizedDescription)
                }
//                print(String(decoding:data ?? Data(), as: UTF8.self))
                if ((error) != nil){
                    print(error)
                }
                
//                print(response)
            }
        )
        task.resume()
        return true
    }
//  
    
    static func Register(user: UserData, identityToken: Data?, authorizationCode: Data?) throws -> Bool {
      print("Saving credentials to the server")
      var url = URL(string:"http://165.232.156.229:8000/users_apple")
      var request = URLRequest(
          url: url!,
          cachePolicy: .reloadIgnoringLocalCacheData
      )
      struct RequestBody:Encodable {
          let user:UserData
          let identityToken: String
          let authorizationCode: String
      }
      let body = try JSONEncoder().encode(RequestBody(user: user, identityToken: String(decoding:identityToken ?? Data(),as:UTF8.self), authorizationCode: String(decoding:authorizationCode ?? Data(),as:UTF8.self)))
      request.httpMethod = "POST"
      request.httpBody = body
      request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
      let task = URLSession.shared.dataTask(
          with: request,
          completionHandler: { data, response, error in
              // Validate response and call handler
              let decoder = JSONDecoder()
              do {
                  let token_response = try decoder.decode(token_response.self, from: data!)
                  print(token_response)
              } catch {
                  print(error.localizedDescription)
              }
//              print(String(decoding:data ?? Data(), as: UTF8.self))
//                print(response)
          }
      )
      task.resume()
      
    return true
  }
}

struct token_response:Codable{
    let access_token:String
    let token_type:String
    let expires_in:Int
    let refresh_token:String
    let id_token:String
}
