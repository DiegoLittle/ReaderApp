//
//  HomeView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/20/22.
//


import SwiftUI
import WebKit
import Alamofire
class ArticleFetcher: ObservableObject {
    lazy var html = ""
    lazy var arxiv = ""
    func test(){
        
//        AF.request("https://en.wikipedia.org/api/rest_v1/page/mobile-html/Dog?footer=true&theme=dark")
//    https://en.wikipedia.org/api/rest_v1/page/html/Dog
//    https://en.wikipedia.org/api/rest_v1/page/mobile-html/Dog?footer=true&theme=dark
        AF.request("https://en.wikipedia.org/api/rest_v1/page/html/Dog")
            .responseString { response in
                self.html = response.value!
//                print(self.html)
        }
//    https://en.wikipedia.org/api/rest_v1/page/html/Dog
        AF.request("https://www.arxiv-vanity.com/papers/1301.3781/").responseString{ response in
            self.arxiv = response.value!
            print(self.arxiv)
            
        }
    }
    init(){
        test()
    }
}

struct HomeView: View {
    
    @State var article = ArticleFetcher()
    
    
  var body: some View {
      WebView(url: URL(string:"https://www.arxiv-vanity.com/papers/1301.3781/")!)
          .frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: .infinity)
          .ignoresSafeArea()
      
  }
}

struct WebView: UIViewRepresentable {
//  @Binding var text: String
    var url:URL
   
  func makeUIView(context: Context) -> WKWebView {
    return WKWebView()
  }
  func updateUIView(_ uiView: WKWebView, context: Context) {
      let request = URLRequest(url:url)
//      uiView.navigationDelegate = self
//      var child = UIHostingController(rootView: HomeView())
//      uiView.bottomAnchor.constraint(equalTo:child.view.bottomAnchor, constant:0).isActive = true
      uiView.load(request)
//    uiView.loadHTMLString(text, baseURL: nil)
  }
    func viewDidLoad(){
        print("Hello World")
    }
}
//
//struct HomeView: View{
//
//
//    var body: some View{
//        Text("Detail View")
//    }
//}

