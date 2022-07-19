//
//  TestView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/21/22.
//

import UIKit
import WebKit
import SwiftUI
import Combine
import Introspect
import SwiftSoup
//let backgroundGradient = LinearGradient(
//    colors: [Color.red, Color.blue],
//    startPoint: .top, endPoint: .bottom)
var searchService = SearchService()
var api = WebApi()
extension UIScreen{
   static let screenWidth = UIScreen.main.bounds.size.width
   static let screenHeight = UIScreen.main.bounds.size.height
   static let screenSize = UIScreen.main.bounds.size
}



class Browser: UIViewController {
    var store: AppStore

    var webView = WKWebView()
    var backButton: UIBarButtonItem?
    var forwardButton: UIBarButtonItem?
    @ObservedObject private var presenter: ContentPresenter
    var url:String = "https://www.arxiv-vanity.com/papers/1301.3781/"
    var query = ""
    var isBookmarked:Bool
    var linkURL:String = ""
    var showSearch:Bool = false
    var menuOpened:Bool = false
    var sections:[section] = []
    var page_description:String = ""
    var bookmark:Bookmark
    init(presenter: ContentPresenter,url:String?,store:AppStore,isBookmarked:Bool=false,showSearch:Bool=false,menuOpened:Bool=false,bookmark:Bookmark = Bookmark()) {
        self.presenter = presenter
        self.url = url ?? "https://google.com/"
        self.store = store
        self.query = ""
        self.isBookmarked = isBookmarked
        self.showSearch = showSearch
        self.menuOpened = menuOpened
        self.bookmark = bookmark

        super.init(nibName: nil, bundle: nil)
        let config = WKWebViewConfiguration()
//        let contentController = WKUserContentController()
//        let source = "document.addEventListener('click', function(){ window.webkit.messageHandlers.iosListener.postMessage('click clack!'); })"
        let source = """
                        document.addEventListener('click', function(e) {
                                var href = e.target.closest('a').href || '';
                                if (e.target.className == 'reference-link'){
                                window.webkit.messageHandlers.iosListener.postMessage('#'+href.split("#")[href.split("#").length-1]);
                        }
                        else{
                        window.webkit.messageHandlers.iosListener.postMessage(href);

                        }
                            });
                        """
        let script = WKUserScript(source: source, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
            config.userContentController.addUserScript(script)
            config.userContentController.add(self, name: "iosListener")
//        let test_source = """
//                        document.addEventListener('click', function(e) {
//                                var href = e.target.closest('a').href || '';
//
//                                window.webkit.messageHandlers.iosListener.postMessage(e.target.className);
//                            });
//                        """
//        let test_script = WKUserScript(source: test_source, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
//            config.userContentController.addUserScript(test_script)
//            config.userContentController.add(self, name: "testListener")
//        config.userContentController = contentController

//        let source = "document.addEventListener('click', function(){ window.webkit.messageHandlers.iosListener.postMessage('click clack!'); })"
//        let script = WKUserScript(source: source, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
//        config.userContentController.addUserScript(script)
//        config.userContentController.add(self, name: "iosListener")
        self.webView = WKWebView(frame: .zero, configuration: config)
    }


    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("This class does not support NSCoder")
    }
    
    @objc func saveBookmark(){
        var bookmark = Bookmark()
        bookmark.url = url
        bookmark.title = self.webView.title
        bookmark.description = self.page_description
        do{
            try api.post_bookmark(bookmark: bookmark)
        }
        catch{
            print("Error posting bookmark to API")
        }
        store.send(.saveBookmark(bookmark))
//        Post request to API
        self.isBookmarked=true
        setBarItems()
        print("Saving Bookmark")
    }
    @objc func deleteBookmark(){
        var bookmark:Bookmark
        for (index,item) in store.state.bookmarks.enumerated(){
            if(item.url == url){
                store.send(.deleteBookmark(item))
                break
            }
        }
        
        self.isBookmarked=false
        setBarItems()
        print("Deleting Bookmark")
    }
    @objc func closeSearch(){
        if(showSearch){
            presenter.navigationController?.popViewController(animated: true)
        }
        else{
        let swiftUIView = searchResultsView(presenter:presenter)
        let hostingController = UIHostingController(rootView: swiftUIView)
        view.bringSubviewToFront(webView)
        view.subviews[0].removeFromSuperview()
        setBarItems()
        navigationItem.hidesBackButton = false
        navigationItem.leftBarButtonItem = nil
        navigationItem.titleView = nil
        self.webView.evaluateJavaScript(
            "document.title"
        ) { (result, error) -> Void in
            self.navigationItem.title = result as? String
        }
        let cssString = "@media (prefers-color-scheme: dark) {body {color: white;}a:link {color: #0096e2;}a:visited {color: #9d57df;}}"
        let jsString = "var style = document.createElement('style'); style.innerHTML = '\(cssString)'; document.head.appendChild(style);"
                webView.evaluateJavaScript(jsString, completionHandler: nil)
        }
    }
    
    @objc func openSearch(){

        navigationItem.hidesBackButton = true
        navigationItem.leftBarButtonItem = UIBarButtonItem(
            image: UIImage(systemName: "xmark")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
            style: .plain,
            target: self,
            action: #selector(closeSearch))
        let swiftUIView = searchResultsView(presenter:presenter).environmentObject(store)
        let hostingController = UIHostingController(rootView: swiftUIView)
        

        /// Add as a child of the current view controller.
        addChild(hostingController)

        /// Add the SwiftUI view to the view controller view hierarchy.
        view.addSubview(hostingController.view)

        /// Setup the constraints to update the SwiftUI view boundaries.
        hostingController.view.translatesAutoresizingMaskIntoConstraints = false
        let constraints = [
            hostingController.view.topAnchor.constraint(equalTo: view.topAnchor),
            hostingController.view.leftAnchor.constraint(equalTo: view.leftAnchor),
            view.bottomAnchor.constraint(equalTo: hostingController.view.bottomAnchor),
            view.rightAnchor.constraint(equalTo: hostingController.view.rightAnchor)
        ]

        NSLayoutConstraint.activate(constraints)

        /// Notify the hosting controller that it has been moved to the current view controller.
        hostingController.didMove(toParent: self)
        navigationItem.titleView = UIHostingController(rootView: searchBarView(presenter:presenter).environmentObject(store)).view
        self.navigationController?.setToolbarHidden(false, animated: true)

//        let textField = UITextField()
//        textField.placeholder = "search"
//        textField.becomeFirstResponder()
//        navigationItem.titleView = textField
    }
    
    @objc func showMenu(){
        self.menuOpened = true
        let menuView = UIHostingController(rootView: MenuView(
            sections:self.sections,
            webview:self.webView,
            browser:self,
            navigationController: self.navigationController!
        ))
//            self.addChild(menuView)
            self.view.addSubview(menuView.view)
        self.navigationController?.setToolbarHidden(false, animated: true)
        
//        view.bringSubviewToFront(webView)
//        view.subviews[0].removeFromSuperview()
        

//        /// Add as a child of the current view controller.
//        addChild(hostingController)
//
//        /// Add the SwiftUI view to the view controller view hierarchy.
//        view.addSubview(hostingController.view)

        /// Setup the constraints to update the SwiftUI view boundaries.
    
//        menuView.additionalSafeAreaInsets()
        menuView.view.translatesAutoresizingMaskIntoConstraints = false
        let guide = view.safeAreaLayoutGuide
        let window = UIApplication.shared.windows.first
        let topPadding = window!.safeAreaInsets.top
        let bottomPadding = window!.safeAreaInsets.bottom
        print(topPadding)
        print(bottomPadding)
        print(-bottomPadding/4)
        let topBarBottom = self.navigationController!.navigationBar.frame.maxY

        func getHeight() -> CGFloat{
            let screenHeight = UIScreen.main.bounds.size.height
            let topBarBottom = self.navigationController!.navigationBar.frame.maxY
//            let toolbarTop = self.navigationController.toolbar.frame.origin.y
//            let originalHeight = screenHeight - toolbarTop
            return screenHeight - topBarBottom
        }
        
//        let constraints = [
//        menuView.view.topAnchor.constraint(equalToConstant:topBarBottom)
//            menuView.view.leftAnchor.constraint(equalTo: view.leftAnchor),
////            menuView.view.bottomAnchor.constraint(equalTo:view.bottomAnchor,constant:bottomPadding)
//
//        ]
        menuView.view.backgroundColor = .clear
//
//        NSLayoutConstraint.activate(constraints)

        /// Notify the hosting controller that it has been moved to the current view controller.
        menuView.didMove(toParent: self)
        self.navigationController?.setToolbarHidden(false, animated: true)
        setBarItems()
    }
    @objc func closeMenu(){
        self.menuOpened=false
        view.bringSubviewToFront(webView)
        print(view.subviews)
        view.subviews[0].removeFromSuperview()
        setBarItems()
//        let textField = UITextField()
//        textField.placeholder = "search"
//        textField.becomeFirstResponder()
//        navigationItem.titleView = textField
    }
    
    @objc func shareMenu(){
        
        guard let data = self.webView.url else { return }
                let av = UIActivityViewController(activityItems: [data], applicationActivities: nil)
                UIApplication.shared.windows.first?.rootViewController?.present(av, animated: true, completion: nil)
    }
    
    func getHTML(_ completion: @escaping (String) -> ()) {
        webView.evaluateJavaScript("document.documentElement.outerHTML") { (html, error) in
            guard let html = html as? String else {
                print(error)
                return
            }
            completion(html)
        }
    }
    
//    func getWikiDescription() -> String{
//        getHTML{ html in
//            do{
//                let doc: Document = try SwiftSoup.parse(html)
//                let section_tags = try doc.getElementsByTag("section")
//
//                return description
//            }
//            catch{
//                print("Error getting wikipedia description")
//            }
//
//        }
//    }
    
    
    
    func webView(_ webView: WKWebView,decidePolicyFor navigationResponse: WKNavigationResponse, decisionHandler: @escaping (WKNavigationResponsePolicy) -> Void) {
//        print(navigationAction.navigationType)
        let response = navigationResponse.response as? HTTPURLResponse
//        print(response?.statusCode)
//        print(response?.allHeaderFields)
//        print(response?.url?.absoluteString)
        var navigationURL = response?.url?.absoluteString
        let webviewURL = URL(string:url)
        if(self.linkURL == navigationURL){
            print(navigationURL)
//            presenter.navToTest(url:navigationURL)
        }
        else{
            decisionHandler(.allow)
            return

        }
//        if let host = navigationAction.request.url?.host {
//            print(host)
//            if host.contains("hackingwithswift.com") {
//                decisionHandler(.allow)
//                return
//            }
//        }
        decisionHandler(.cancel)
    }
    
    func setBarItems(){
        func setArrows(){
            
        }
        self.navigationController?.setToolbarHidden(false, animated: true)
        var hamburgerButton:UIBarButtonItem
        if(self.menuOpened){
            hamburgerButton = UIBarButtonItem(
                        image: UIImage(systemName: "text.insert")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                        style: .plain,
                        target: self,
                        action: #selector(closeMenu))
        }
        else{
            hamburgerButton = UIBarButtonItem(
                        image: UIImage(systemName: "text.insert")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                        style: .plain,
                        target: self,
                        action: #selector(showMenu))
        }

        for bookmark in store.state.bookmarks {
            if(bookmark.url==url){
                self.isBookmarked = true
            }
        }
        var bookmarkButton:UIBarButtonItem

        if(self.isBookmarked){
            print("isBookmarked")
            bookmarkButton = UIBarButtonItem(
                image: UIImage(systemName: "bookmark.fill")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                style: .plain,
                target: self,
                action: #selector(deleteBookmark))
        }
        else{
            print("Is not bookmarked")
            bookmarkButton = UIBarButtonItem(
                image: UIImage(systemName: "bookmark")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                style: .plain,
                target: self,
                action: #selector(saveBookmark))
        }

    

        let reloadButton = UIBarButtonItem(
                   image: UIImage(systemName: "arrow.counterclockwise")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                   style: .plain,
                   target: self.webView,
                   action: #selector(WKWebView.reload))
        let shareButton = UIBarButtonItem(
                   image: UIImage(systemName: "square.and.arrow.up")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                   style: .plain,
                   target: self,
                   action: #selector(shareMenu))
        if(!self.url.starts(with: "https://en.wikipedia.org")){
        let backButton = UIBarButtonItem(
                    image: UIImage(systemName: "arrow.left")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
                    style: .plain,
                    target: self.webView,
                    action: #selector(WKWebView.goBack))
        let forwardButton = UIBarButtonItem(
            image: UIImage(systemName: "arrow.right")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
            style: .plain,
            target: self.webView,
            action: #selector(WKWebView.goForward))

                self.toolbarItems = [hamburgerButton,backButton, forwardButton,
                                     UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil),
                                     bookmarkButton,
                                     UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil),
                                     shareButton,
                                     UIBarButtonItem(barButtonSystemItem: .fixedSpace, target: nil, action: nil),
                                     reloadButton
//                                     bookmarkButton
                ]
        }
        else{
            self.toolbarItems = [hamburgerButton,
                                 UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil),
                                 bookmarkButton,
                                 UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil),
                                 shareButton,
                                 UIBarButtonItem(barButtonSystemItem: .fixedSpace, target: nil, action: nil),
                                 reloadButton
//                                     bookmarkButton
            ]

        }
//        print(self.navigationController?.toolbar.frame.height)
//        print(self.navigationController?.toolbar.frame)
//        self.navigationController?.toolbar.frame = CGRect(x: 0, y: 0, width: self.view.frame.size.width, height: 20.0)
//        self.navigationController?.navigationBar.
        navigationItem.rightBarButtonItem =  UIBarButtonItem(
            image: UIImage(systemName: "magnifyingglass")!.withTintColor(.blue, renderingMode: .alwaysTemplate),
            style: .plain,
            target: self,
            action: #selector(openSearch))
//
//                self.backButton = backButton
//                self.forwardButton = forwardButton
        
    }
    override func viewDidLoad() {
        print("Loading webview")
        if(self.showSearch){
            print("Opening search")
            openSearch()

        }

        else{
        self.view.addSubview(webView)
        

        self.webView.translatesAutoresizingMaskIntoConstraints = false
        self.webView.topAnchor.constraint(equalTo: self.view.topAnchor).isActive = true
//        webView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 0.0).isActive = true

        self.webView.bottomAnchor.constraint(equalTo: self.view.bottomAnchor).isActive = true
        self.webView.leadingAnchor.constraint(equalTo: self.view.leadingAnchor).isActive = true
        self.webView.trailingAnchor.constraint(equalTo: self.view.trailingAnchor).isActive = true
            self.webView.load(URLRequest(url: URL(string:url) ?? URL(string:"https://google.com")!))
        self.webView.navigationDelegate = self
        
        
            self.bookmark.url = self.bookmark.url ?? self.url
            self.bookmark.title = self.bookmark.title ?? self.webView.title
            if(self.bookmark.title == ""){
                if(self.webView.title == ""){
                    self.bookmark.title = "Add a title"
                }
                   else{
                    self.bookmark.title = self.webView.title
                }
            }
            if(self.bookmark.description == ""){
                self.bookmark.description = self.page_description
            }
            var swiftUIView:PageTitle
            swiftUIView = PageTitle(title:self.bookmark.title!,presenter:presenter,bookmark:self.bookmark)
//                if(bookmark.title == "" || bookmark.title == nil){
//                swiftUIView = PageTitle(title:self.webView.title!,presenter:presenter,bookmark:self.bookmark)
//                }
//                else{
//                    swiftUIView = PageTitle(title:bookmark.title!,presenter:presenter,bookmark:self.bookmark)
//                }
            var hosting = UIHostingController(rootView: swiftUIView.environmentObject(store)).view
            hosting?.backgroundColor = .clear
            navigationItem.titleView = hosting
            
            
        self.webView.allowsBackForwardNavigationGestures = true
        self.webView.addObserver(self, forKeyPath: #keyPath(WKWebView.title), options: .new, context: nil)
        
//        showMenu()
        setBarItems()

        }
        


    }
    override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?) {
            if keyPath == #keyPath(WKWebView.title) {
                
                
                
//                self.navigationItem.title = self.webView.title
//                let label = UILabel()
//                label.text = self.webView.title
//                label.
                self.bookmark.url = self.bookmark.url ?? self.url
                self.bookmark.title = self.bookmark.title ?? self.webView.title
                if(self.bookmark.title == "" || self.bookmark.title == "Add a title"){
                    if(self.webView.title == ""){
                        self.bookmark.title = "Add a title"
                    }
                       else{
                        self.bookmark.title = self.webView.title
                    }
                }
                if(self.bookmark.description == ""){
                    self.bookmark.description = self.page_description
                }
                var swiftUIView:PageTitle
                print("webview title observed")
                print(self.bookmark.title!)
                swiftUIView = PageTitle(title:self.bookmark.title!,presenter:presenter,bookmark:self.bookmark)
    //                if(bookmark.title == "" || bookmark.title == nil){
    //                swiftUIView = PageTitle(title:self.webView.title!,presenter:presenter,bookmark:self.bookmark)
    //                }
    //                else{
    //                    swiftUIView = PageTitle(title:bookmark.title!,presenter:presenter,bookmark:self.bookmark)
    //                }
                var hosting = UIHostingController(rootView: swiftUIView.environmentObject(store)).view
                hosting?.backgroundColor = .clear
                navigationItem.titleView = hosting
//                UIHostingController(rootView: searchBarView(presenter:presenter).environmentObject(store)).view
            }
        if let _ = object as? WKWebView {
            if keyPath == #keyPath(WKWebView.canGoBack) {
                self.backButton?.isEnabled = self.webView.canGoBack
            } else if keyPath == #keyPath(WKWebView.canGoForward) {
                self.forwardButton?.isEnabled = self.webView.canGoForward
            }
        }
        }

}
struct section: Identifiable{
    let id:UUID = UUID()
    let selector: String
    let section_title: String
    var subsections: [section] = []

}
func isDuplicate(subsection:section,subsections:[section]){
    for item in subsections{
        print(item.section_title)
        print(subsection.section_title)
    }
    
}
extension Browser: WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        self.webView.evaluateJavaScript(
            "document.title"
        ) { (result, error) -> Void in
            self.navigationItem.title = result as? String
        }
        getHTML{ html in
            do {
                var html_sections:[section] = []
                let doc: Document = try SwiftSoup.parse(html)
                let header_tag = try doc.select("#pcs > header > div > h1").text()
                let header_section = section(
                    selector: "#pcs > header > div > h1", section_title: header_tag
                )
                
                html_sections.append(header_section)
                let section_tags = try doc.getElementsByTag("section")
                if(self.url.starts(with: "https://en.wikipedia.org")){
                    let description_node = section_tags.first
                    let description = try description_node?.text()
                    self.page_description = description ?? ""

                }
                
                for tag in section_tags{
                    let section_title = try! tag.select("h2").text()
                    var subsections:[section] = []
                    let sub_headers = try tag.select("h3")
                    if(!(section_title=="References")){
                    for (index, sub_header) in sub_headers.enumerated() {
                        let subsection = section(
                            selector:try! sub_header.cssSelector(),
                            section_title: try sub_header.text()
                        )
//                        print(subsection)
//                        print(subsections)

                        print(isDuplicate(subsection: subsection,subsections: subsections))
//                        if(!subsections.contains(subsection)){
//                            subsections.append(subsection)
//                        }
                        subsections.append(subsection)

                    }
                    }
                    
                    if(!section_title.isEmpty){
                        var section = section(
                            selector:try! tag.cssSelector(),
                            section_title: section_title
                        )
                        section.subsections = subsections
                        html_sections.append(section)
                        
                    }
                }
                self.sections = html_sections
                print(self.sections)
                

            } catch Exception.Error(let type, let message) {
                print("")
            } catch {
                print("")
            }
        }
        
        
    }
}
extension Browser: WKScriptMessageHandler {
  func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
      
      print("Received link click event")
      print(message.body)
      print(message.name)
      let href = String(describing:message.body)
      if href.starts(with: "#"){
          print("Relative link")
          self.webView.evaluateJavaScript(
              "document.querySelector('#References').scrollIntoView({behavior: 'smooth'});"
          )
          self.webView.evaluateJavaScript(
            "document.querySelector('#References').click()"
          )
          print("document.querySelector('"+href+"').scrollIntoView({behavior: 'smooth'});")
          self.webView.evaluateJavaScript(
              "document.querySelector('"+href+"').scrollIntoView({behavior: 'smooth'});"
          )
      }
//      var message_url = String(describing:message.body).removingPercentEncoding ?? ""
      else if(String(describing:message.body).starts(with: "https://en.wikipedia.org/wiki/")){
          print("A wikipedia link!")
//
              let result = String(describing:message.body).components(separatedBy:"https://en.wikipedia.org/wiki/")[1]
              var color = UITraitCollection.current.userInterfaceStyle == .dark ? "dark" : "light"
              var url = "https://en.wikipedia.org/api/rest_v1/page/mobile-html/"+result+"?footer=true&theme="+color
              var urlString = url.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed)
              presenter.navToTest(url:urlString!)
//          }
          

      }
      else{
          presenter.navToTest(url:String(describing: message.body))
      }
      self.linkURL = String(describing: message.body)
      if message.name == "test", let messageBody = message.body as? String {
          print(messageBody)
      }
  }
}
  


struct PageTitle: View{
    @State var title:String
    @State var editMode:Bool = false
    @ObservedObject var presenter: ContentPresenter
    @EnvironmentObject var store: AppStore
    @State var bookmark:Bookmark
    var api = WebApi()
    var body: some View{
        VStack(alignment:.center){
            if(editMode){
                TextField("", text: $title,onCommit: {
                    print(title)
                    bookmark.title = title
                    store.send(.updateBookmark(bookmark))
                    Task{
                        do{
                            try api.update_bookmark(bookmark: bookmark)
                        }
                    }
//                    Update redux state for the bookmark
//                    PUT request to update serverside
                })
                .font(Font.custom("HelveticaNeue-Medium", size: 17))

            }
            else{
            Text(title)
                .onTapGesture(count: 2) {
                    editMode = true
                    
                    print("Double tapped!")
                }
                .font(Font.custom("HelveticaNeue-Medium", size: 17))
                .background(Color.clear)
            }
        }.padding([.bottom],3)
            .onAppear(perform:{
                print("Page Title Appeared")
            })

    }
}
