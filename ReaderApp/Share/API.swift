//
//  API.swift
//  Share
//
//  Created by Diego Little on 5/1/22.
//

import Foundation
import Alamofire
import MultipartForm

struct pdf_response:Codable{
let isArXiv:Bool
}
func upload_pdf(user_id:String,refresh_token:String,filename:String,data:Data,completionHandler:@escaping (Bool)-> Void) throws -> Bool {
  print("Saving credentials to the server")
//  var url = URL(string:"http://165.232.156.229:8000/pdf")
    var url = URLComponents(string: "http://165.232.156.229:8000/pdf")!


    let form = MultipartForm(parts: [
        MultipartForm.Part(name: "file", data: data, filename: filename, contentType: "application/pdf"),
    ])
    url.queryItems = [
        URLQueryItem(name: "refresh_token", value: refresh_token),
        URLQueryItem(name:"user_id",value:user_id)
    ]

    var request = URLRequest(url: url.url!)
    request.httpMethod = "POST"
    request.setValue(form.contentType, forHTTPHeaderField: "Content-Type")

    let task = URLSession.shared.uploadTask(with: request, from: form.bodyData,completionHandler: {data, response, error in
        do {
            let decoder = JSONDecoder()
            print(data)
            print(response)
            let pdf_response = try decoder.decode(pdf_response.self, from: data!)
            completionHandler(pdf_response.isArXiv)
        } catch  {
            print("Error decoding response")
        }
    })
    task.resume()
//  var request = URLRequest(
//      url: url!,
//      cachePolicy: .reloadIgnoringLocalCacheData
//  ) let image = UIImage.init(named: "myImage")
//    let imgData = UIImageJPEGRepresentation(image!, 0.2)!
//
//    let parameters = ["name": rname] //Optional for extra parameter

//    fileprivate func uploadDocument(_ file: Data,filename : String,handler : @escaping (String) -> Void) {
//
//       }
   
////    try post()
//    AF.upload(
//            multipartFormData: {
//                multipartFormData in
//
//                if let urlString = urlBase2 {
////                    let pdfData = try! Data(contentsOf: urlString.asURL())
////                    var data : Data = pdfData
//
//                    multipartFormData.append(pdfData, withName: "pdfDocuments", fileName: namePDF, mimeType:"application/pdf")
//                    for (key, value) in body {
//                        multipartFormData.append(((value as? String)?.data(using: .utf8))!, withName: key)
//                    }
//
//                    print("Multi part Content -Type")
//                    print(multipartFormData.contentType)
//                    print("Multi part FIN ")
//                    print("Multi part Content-Length")
//                    print(multipartFormData.contentLength)
//                    print("Multi part Content-Boundary")
//                    print(multipartFormData.boundary)
//                }
//        },
//            to: url!,
//            method: .post,
////            headers: header,
//            encodingCompletion: { encodingResult in
//
//                switch encodingResult {
//
//                case .success(let upload, _, _):
//                    upload.responseJSON { response in
//                        print(" responses ")
//                        print(response)
//                        print("Responses ended")
//
//                        onCompletion(true, "Something went wrong", 200)
//
//                    }
//                case .failure(let encodingError):
//                    print(encodingError)
//                    onCompletion(false, "Something went wrong", 200)
//                }
//        })
//    var request = MultipartFormDataRequest(url: URL(string: "http://165.232.156.229:8000/pdf")!)
//    request.addDataField(named: "profilePicture", data: data, mimeType: "application/pdf")
////  request.httpMethod = "POST"
////  request.httpBody = body
////  request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
//  let task = URLSession.shared.uploadTask(
//    with: request.asURLRequest(),
//      from: data,
//      completionHandler: { data, response, error in
//          // Validate response and call handler
//          print(String(data: data!, encoding: .utf8))
////          let decoder = JSONDecoder()
////          do {
////              let token_response = try decoder.decode(token_response.self, from: data!)
////              print(token_response)
////          } catch {
////              print(error.localizedDescription)
////          }
////              print(String(decoding:data ?? Data(), as: UTF8.self))
////                print(response)
//      }
//  )
//  task.resume()
  
return true
}
struct DummyData: Codable {
  /// The email address to use for user communications.  Remember it might be a relay!
  let email: String

  /// The components which make up the user's name.  See `displayName(style:)`
  let name: String

  /// The team scoped identifier Apple provided to represent this user.
  let identifier: String
}
func post() throws -> Void{
    var url = URL(string:"http://165.232.156.229:8000/pdf")
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


//extension URLSession {
//    func dataTask(with request: MultipartFormDataRequest,
//                  completionHandler: @escaping (Data?, URLResponse?, Error?) -> Void)
//    -> URLSessionDataTask {
//        return dataTask(with: request.asURLRequest() as! MultipartFormDataRequest, completionHandler: completionHandler)
//    }
//}


struct MultipartFormDataRequest {
    private let boundary: String = UUID().uuidString
    private var httpBody = Data()
    let url: URL

    init(url: URL) {
        self.url = url
    }
    mutating func asURLRequest() -> URLRequest {
        var request = URLRequest(url: url)

        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        httpBody.append(Data("--\(boundary)--".utf8))
        request.httpBody = httpBody
        print(request.allHTTPHeaderFields)
        print(request.httpBody)
        return request
    }
    mutating func addTextField(named name: String, value: String) {
        httpBody.append(Data(textFormField(named: name, value: value).utf8))
    }

    private func textFormField(named name: String, value: String) -> String {
        var fieldString = "--\(boundary)\r\n"
        fieldString += "Content-Disposition: form-data; name=\"\(name)\"\r\n"
        fieldString += "Content-Type: text/plain; charset=ISO-8859-1\r\n"
        fieldString += "Content-Transfer-Encoding: 8bit\r\n"
        fieldString += "\r\n"
        fieldString += "\(value)\r\n"

        return fieldString
    }

    mutating func addDataField(named name: String, data: Data, mimeType: String) {
        httpBody.append(dataFormField(named: name, data: data, mimeType: mimeType))
    }

    private func dataFormField(named name: String,
                               data: Data,
                               mimeType: String) -> Data {
        var fieldData = Data()

        fieldData.append(Data("--\(boundary)\r\n".utf8))
        fieldData.append(Data("Content-Disposition: form-data; name=\"\(name)\"\r\n".utf8))
        fieldData.append(Data("Content-Type: \(mimeType)\r\n".utf8))
        fieldData.append(Data("\r\n".utf8))
        fieldData.append(data)
        fieldData.append(Data("\r\n".utf8))

        return fieldData as Data
    }
}

extension NSMutableData {
  func append(_ string: String) {
    if let data = string.data(using: .utf8) {
      self.append(data)
    }
  }
}

func uploadFile(paramName: String, fileName: String, data: Data,mimeType:String) {
    let url = URL(string: "http://api-host-name/v1/api/uploadfile/single")

    // generate boundary string using a unique per-app string
    let boundary = UUID().uuidString

    let session = URLSession.shared

    // Set the URLRequest to POST and to the specified URL
    var urlRequest = URLRequest(url: url!)
    urlRequest.httpMethod = "POST"

    // Set Content-Type Header to multipart/form-data, this is equivalent to submitting form data with file upload in a web browser
    // And the boundary is also set here
    urlRequest.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

    var data = Data()

    // Add the image data to the raw http request data
    data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
    data.append("Content-Disposition: form-data; name=\"\(paramName)\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
    data.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
    data.append(data)

    data.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

    // Send a POST request to the URL, with the data we created earlier
    session.uploadTask(with: urlRequest, from: data, completionHandler: { responseData, response, error in
        if error == nil {
            let jsonData = try? JSONSerialization.jsonObject(with: responseData!, options: .allowFragments)
            if let json = jsonData as? [String: Any] {
                print(json)
            }
        }
    }).resume()
}
