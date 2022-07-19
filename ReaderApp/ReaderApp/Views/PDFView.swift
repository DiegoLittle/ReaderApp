//
//  PDFView.swift
//  ReaderApp
//
//  Created by Diego Little on 4/26/22.
//

import Foundation
import UIKit
import PDFKit
import SwiftUI


class PDFViewController: UIViewController {
    @ObservedObject private var presenter: ContentPresenter
    var store: AppStore
    var path:String
    var bookmark:Bookmark
    init(presenter:ContentPresenter,store:AppStore,path:String,bookmark:Bookmark){
        self.presenter = presenter
        self.store = store
        self.path = path
        self.bookmark = bookmark
        super.init(nibName: nil, bundle: nil)
    }
    @available(*, unavailable)
    required init?(coder: NSCoder) {
        fatalError("This class does not support NSCoder")
    }
    override func viewDidLoad() {
        let pdfView = PDFView()

        pdfView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(pdfView)

        pdfView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor).isActive = true
        pdfView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor).isActive = true
        pdfView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor).isActive = true
        pdfView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor).isActive = true
        print("PDF Path: ")
//        print(path)
//        guard let pdf_path = Bundle.main.url(forResource: path, withExtension: "pdf") else { return }
//        print("PDF Path: ")
//        print(pdf_path)
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
        let filemgr = FileManager.default
        
//        filename = filename as! String
        var sharedDir = FileManager.sharedContainerURL().absoluteString.components(separatedBy: "file://")[1]
        var filepath = sharedDir+self.path
        print(filepath)
        let databuffer = filemgr.contents(atPath: filepath) ?? Data()
        print(databuffer)
        if let document = PDFDocument(data:databuffer) {
            pdfView.document = document
        }
        var swiftUIView:PageTitle
        if(bookmark.title == ""){
        swiftUIView = PageTitle(title:"",presenter:presenter,bookmark:self.bookmark)
        }
        else{
            swiftUIView = PageTitle(title:bookmark.title!,presenter:presenter,bookmark:self.bookmark)
        }
        var hosting = UIHostingController(rootView: swiftUIView.environmentObject(store)).view
        hosting?.backgroundColor = .clear
        navigationItem.titleView = hosting
//        navigationItem.title = bookmark.title
//        var filename:String? = sharedDefault.object(forKey: "pdf_path") as? String
//        print(filename)
//        if let file = filename {
//            let filemgr = FileManager.default
//    //        filename = filename as! String
//            var sharedDir = FileManager.sharedContainerURL().absoluteString.components(separatedBy: "file://")[1]
//            var filepath = sharedDir+file
//            print(filepath)
//            let databuffer = filemgr.contents(atPath: filepath) ?? Data()
//            print(databuffer)
//            if let document = PDFDocument(data:databuffer) {
//                pdfView.document = document
//            }
//        }

    }
}

extension FileManager {
  static func sharedContainerURL() -> URL {
    return FileManager.default.containerURL(
      forSecurityApplicationGroupIdentifier: "group.synesthesia.ReaderApp"
    )!
  }
}
