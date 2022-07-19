//
//  ShareViewController.swift
//  Share
//
//  Created by Diego Little on 4/26/22.
//

import UIKit
import Social
import MobileCoreServices
struct Bookmark: Identifiable, Equatable,Codable{
    var id:UUID = UUID()
    var url:String?
    var title:String?
    var type:String? = "web"
}

enum ShareItem {
    case unknown
    case bookmark
    case pdf
}

class ShareViewController: SLComposeServiceViewController {
    
    func shareType(inputItem:NSExtensionItem) -> ShareItem{
        print("Getting share type")
        var hasURL:Bool = false
        var hasText:Bool = false
        var hasPDF:Bool = false
        var hasFileURL:Bool = false
        for (index, _) in (inputItem.attachments?.enumerated())! {
            if let itemProvider = inputItem.attachments?[index] as? NSItemProvider {
                print(itemProvider)
                    print(type(of: itemProvider))
                    print(itemProvider.registeredTypeIdentifiers)
                let typeIDS = itemProvider.registeredTypeIdentifiers
    //                ["public.plain-text"]
//                print(itemProvider)
                if(typeIDS.contains("com.adobe.pdf")){
                    hasPDF = true
                }
                if(typeIDS.contains("public.file-url")){
                hasFileURL = true
                }
                    print("Item provider type identifiers:")
                   print( itemProvider.registeredTypeIdentifiers)
                    if(itemProvider.hasItemConformingToTypeIdentifier("public.url")){
                        hasURL = true
                    }
                    else if(itemProvider.hasItemConformingToTypeIdentifier("public.plain-text")){
                        hasText = true
                    }
                else if(itemProvider.hasItemConformingToTypeIdentifier("com.adobe.pdf")){
                    hasPDF = true
                }

//                            // print out the registered type identifiers so we can see what's there
//                            itemProvider.registeredTypeIdentifiers.forEach {  print(String(describing: $0)) }
            }
        }
        print(hasURL)
        print(hasText)
        print(hasPDF)
        print(hasFileURL)
        if(hasPDF){
            return .pdf
        }
        if(hasURL){
            return .bookmark
        }
        return .unknown
    }
    
    func writeBookmark(){
        print("Writing bookmark to shared data")
        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
        var bookmarks:Array = sharedDefault.object(forKey: "syncing_bookmarks") as? Array<Any> ?? []
//                            if bookmarks == nil {
//                                bookmarks = []
//                            }
        
        var bookmark_title = sharedDefault.object(forKey: "bookmark_title") ?? ""
        var bookmark_url = sharedDefault.object(forKey: "bookmark_url")
        print("Writing bookmark to shared data")
        
        let bookmark = Bookmark(
            url: bookmark_url! as! String, title: bookmark_title as! String
        )
        print(bookmark)
        do {
            // Create JSON Encoder
            let encoder = JSONEncoder()

            // Encode Note
            let data = try encoder.encode(bookmark)
            bookmarks.append(data)
    //        print(bookmark)
            sharedDefault.set(bookmarks, forKey: "syncing_bookmarks")
    //                            Read data
            sharedDefault.removeObject(forKey: "bookmark_title")
            sharedDefault.removeObject(forKey: "bookmark_url")

              let mySharableData = sharedDefault.object(forKey: "syncing_bookmarks")
    //        // do what you want to do with shareURL
            print(mySharableData!)
            // Write/Set Data
//            UserDefaults.standard.set(data, forKey: "note")

        } catch {
            print("Unable to Encode Note (\(error))")
        }
        
    }

    override func isContentValid() -> Bool {
        // Do validation of contentText and/or NSExtensionContext attachments here
        return true
    }
    func saveBookmark(inputItem:NSExtensionItem){
        var item_title:String?
        var item_url:String?
        for (index, _) in (inputItem.attachments?.enumerated())! {
            
            if let itemProvider = inputItem.attachments?[index] as? NSItemProvider {
                    print(type(of: itemProvider))
                    print(itemProvider.registeredTypeIdentifiers)
    //                ["public.plain-text"]
                    print("Item provider type identifiers:")
                   print( itemProvider.registeredTypeIdentifiers)
                    if(itemProvider.hasItemConformingToTypeIdentifier("public.url")){
                        itemProvider.loadItem(forTypeIdentifier: "public.url", options: nil) { (url, error) in
                            if let shareURL = url as? URL {

    //                            Write Data
                                let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
                                print(shareURL)
                                print(type(of: shareURL))
                                item_url = shareURL.absoluteString
                                print("Writing temp url")
                                print(item_url)
                                if let bm_url = item_url {
                                    print(bm_url)
                                    sharedDefault.set(bm_url,forKey: "bookmark_url")
                                    print(bm_url)
                                    print(index==inputItem.attachments!.count-1)
                                    if(index==inputItem.attachments!.count-1){
                                        print("Last item in attatchments")
    //                                    Write the bookmark to the bookmarks array and delete the saved title and url                 writ
                                        self.writeBookmark()
                                        
                                        
    //                                    index==inputItem.attachments!.count+1
                                    }
                                }
                                

                                print(index)
                                print(inputItem.attachments!.count-1)
    //                            var bookmarks:[String] = []

                            }
//                                self.extensionContext?.completeRequest(returningItems: [], completionHandler:nil)
                        }
                    }
                    else if(itemProvider.hasItemConformingToTypeIdentifier("public.plain-text")){
                        itemProvider.loadItem(forTypeIdentifier: "public.plain-text") { (data, error) in
//                                if let shareURL = url as? URL {
                                let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
    //                            Write Data
                                print(data!)
                            item_title = data as! String
                            print("Writing temp url")
                            print(item_title)
                            if let title = item_title{
                                sharedDefault.set(title,forKey: "bookmark_title")
                                
                                print(title)
                                print(index==inputItem.attachments!.count-1)
                                if(index==inputItem.attachments!.count-1){
                                    print("Last item in attatchments")
//                                    Write the bookmark to the bookmarks array and delete the saved title and url                 writ
                                    self.writeBookmark()
                                    
                                    
//                                    index==inputItem.attachments!.count+1
                                }
                            }


//                                    print(type(of: data))
    //
//                                }
//                                self.extensionContext?.completeRequest(returningItems: [], completionHandler:nil)
                        }
                    }

//                            // print out the registered type identifiers so we can see what's there
//                            itemProvider.registeredTypeIdentifiers.forEach {  print(String(describing: $0)) }
            }
        }
        self.extensionContext!.completeRequest(returningItems: [], completionHandler: nil)
        
    }
    func savePDF(inputItem:NSExtensionItem){
        var item_url:String?
        for (index, _) in (inputItem.attachments?.enumerated())! {

            if let itemProvider = inputItem.attachments?[index] as? NSItemProvider {
                    print(type(of: itemProvider))
                    print(itemProvider.registeredTypeIdentifiers)
    //                ["public.plain-text"]
                    print("Item provider type identifiers:")
                   print( itemProvider.registeredTypeIdentifiers)
//                itemProvider.loadItem(forTypeIdentifier: "public.file-url"){ (data,error) in
//                    print(data)
//
//                }
                itemProvider.loadItem(forTypeIdentifier: "public.file-url" as String,options:nil){ (data,error) in
                    if let shareURL = data as? URL{
                        print(shareURL)
//
//                        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//
//                        var path = shareURL.absoluteString.components(separatedBy: "file://")[1]
//                        sharedDefault.set(path.components(separatedBy: "/").last!,forKey: "pdf_path")
//
//                        print(path)
//                        print()
//                        let filename = path.components(separatedBy: "/").last!
//                        print(filename)
////                        var filepath = FileManager.sharedContainerURL().absoluteString+path.components(separatedBy: "/").last!
//                        var filepath = FileManager.sharedContainerURL().appendingPathComponent(filename).path
//                        print(filepath)
//                        let filemgr = FileManager.default
//                        let databuffer = filemgr.contents(atPath: path)
//                        print(databuffer)
//                        do{
//                            let data = try Data(contentsOf: shareURL)
//                        }
//                        catch{
//                            print("Error reading data from file")
//                        }
                        
//                        print(FileManager.sharedContainerURL())
              
                        

                    }
                }
                itemProvider.loadItem(forTypeIdentifier: "com.adobe.pdf" as String,options:nil){ (data,error) in
                    if let shareURL = data as? URL{
                        print(shareURL)
                        let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!

                        var path = shareURL.absoluteString.components(separatedBy: "file://")[1]
                        sharedDefault.set(path.components(separatedBy: "/").last!,forKey: "pdf_path")
                        let filename = path.components(separatedBy: "/").last!
                        var filepath = FileManager.sharedContainerURL().appendingPathComponent(filename).path
//                        print(path)
//                        var filepath = FileManager.sharedContainerURL().absoluteString+path.components(separatedBy: "/").last!
                        print(filepath)
                        let filemgr = FileManager.default
                        let databuffer = filemgr.contents(atPath: path)
                        print(databuffer)
//                        do{
//                            let data = try Data(contentsOf: shareURL)
//                        }
//                        catch{
//                            print("Error reading data from file")
//                        }
                        
//                        print(FileManager.sharedContainerURL())
                        if let data = databuffer {
                            print("Writing data to file")
                            print(data)
                            print(filepath)
//                            filemgr.createFile(atPath:FileManager.sharedContainerURL().appendingPathComponent("share.txt").path,contents:"Hello World".data(using:.utf8))
                            filemgr.createFile(atPath: filepath, contents: data)
                            var isArXiv:Bool = false
                            if let range = data.range(of: "arXivStAmP".data(using: .utf8)!) {
                                print("Found at", range.lowerBound, "..<", range.upperBound)
                                isArXiv = true
                                // Found at 2 ..< 4
                            }
                            print(isArXiv)
                            var bookmark:Bookmark
                            if(isArXiv){
                                bookmark = Bookmark(
                                    url: filename as! String, title: filename as! String, type: "arxiv_paper"
                                )
                            }
                            else{
                                bookmark = Bookmark(
                                    url: filename as! String, title: filename as! String, type: "pdf"
                                )
                            }
                            do {
                                var bookmarks:Array = sharedDefault.object(forKey: "syncing_bookmarks") as? Array<Any> ?? []
                                // Create JSON Encoder
                                let encoder = JSONEncoder()
                                print(bookmark)
                                // Encode Note
                                let data = try encoder.encode(bookmark)
                                bookmarks.append(data)
                        //        print(bookmark)
                                sharedDefault.set(bookmarks, forKey: "syncing_bookmarks")
                                  let mySharableData = sharedDefault.object(forKey: "syncing_bookmarks")
                        //        // do what you want to do with shareURL
                                print(mySharableData!)
                                // Write/Set Data
                    //            UserDefaults.standard.set(data, forKey: "note")

                            } catch {
                                print("Unable to Encode Note (\(error))")
                            }
                            
//                            do {
//
//                                let refresh_token_object = sharedDefault.object(forKey: "refresh_token") as? String
//                                let user_id_object = sharedDefault.object(forKey: "user_id" ) as? String
//                                if let user_id = user_id_object {
//
//                                if let refresh_token = refresh_token_object {
//                                    try upload_pdf(user_id:user_id,refresh_token: refresh_token,filename:filename,data:data){
//                                        isArxiv in
//                                        var bookmark:Bookmark
//                                        if(isArxiv){
//                                            bookmark = Bookmark(
//                                                url: filename as! String, title: filename as! String, type: "arxiv_paper"
//                                            )
//                                        }
//                                        else{
//                                            bookmark = Bookmark(
//                                                url: filename as! String, title: filename as! String, type: "pdf"
//                                            )
//                                        }
//
//                                        do {
//                                            var bookmarks:Array = sharedDefault.object(forKey: "syncing_bookmarks") as? Array<Any> ?? []
//                                            // Create JSON Encoder
//                                            let encoder = JSONEncoder()
//                                            print(bookmark)
//                                            // Encode Note
//                                            let data = try encoder.encode(bookmark)
//                                            bookmarks.append(data)
//                                    //        print(bookmark)
//                                            sharedDefault.set(bookmarks, forKey: "syncing_bookmarks")
//                                              let mySharableData = sharedDefault.object(forKey: "syncing_bookmarks")
//                                    //        // do what you want to do with shareURL
//                                            print(mySharableData!)
//                                            // Write/Set Data
//                                //            UserDefaults.standard.set(data, forKey: "note")
//
//                                        } catch {
//                                            print("Unable to Encode Note (\(error))")
//                                        }
//
//
//                                    }
//                                }
//                                else{
//                                    print("Couldn't authenticate user")
//                                }
//                                }
//                                else{
//                                    print("Couldn't find user")
//                                }
//                            } catch  {
//                            }
                            do {
                                let dir = try FileManager.default.contentsOfDirectory(atPath:FileManager.sharedContainerURL().path)
                                print(dir)
                            } catch {
                                print("Error reading directory")
                            }
                            self.extensionContext!.completeRequest(returningItems: [], completionHandler: nil)
                        }

                    }
                }
                
//                    if(itemProvider.hasItemConformingToTypeIdentifier("public.url")){
//                        itemProvider.loadItem(forTypeIdentifier: "public.url", options: nil) { (url, error) in
//                            if let shareURL = url as? URL {
//
//    //                            Write Data
//                                let sharedDefault = UserDefaults(suiteName: "group.synesthesia.ReaderApp")!
//                                print(shareURL)
//                                print(type(of: shareURL))
//                                item_url = shareURL.absoluteString
//
//                                print("Writing temp url")
//                                print("Storing PDF Document to storage")
//                                print(item_url!)
//                                var path = item_url!.components(separatedBy: "file://")[1]
//                                sharedDefault.set(path,forKey: "pdf_path")
//                                print(path)
//                                let filemgr = FileManager.default
//                                let databuffer = filemgr.contents(atPath: path)
//                                print(databuffer)
//                                //                                print(databuffer)
//
////                                filemgr.
////                                let documentsDirectory =
////                                    FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
////                                let results =
////                                    try? FileManager.default.contentsOfDirectory(at: documentsDirectory,includingPropertiesForKeys: nil)
////                                print(documentsDirectory)
////                                print(results)
////                                print(filemgr.temporaryDirectory)
////                                print(filemgr.fileExists(atPath: path))
////                                let databuffer = filemgr.contents(atPath: path)
////                                print(databuffer)
//
//////                                let url = URL(fileURLWithPath: item_url!)
////                                do {
////                                    let data = try Data(contents: url)
////                                    print(data)
////                                } catch {
////                                    print("Error reading data")
//////                                    Error
////                                }
//
////                                print(index)
////                                print(inputItem.attachments!.count-1)
//                            }
//                        }
//                    }
//
            }
        }
//
    }

    override func didSelectPost() {
        // This is called after the user selects Post. Do the upload of contentText and/or NSExtensionContext attachments.
        print("User Selected post")
        if let inputItem = extensionContext?.inputItems.first as? NSExtensionItem {

            var inputType:ShareItem = shareType(inputItem: inputItem)
            switch inputType {
            case .bookmark:
                saveBookmark(inputItem: inputItem)
            case .pdf:
                savePDF(inputItem: inputItem)
            case.unknown:
                print("Unknown type")
            default:
                print("Unknown type")
            }
            

            
        }
    
        // Inform the host that we're done, so it un-blocks its UI. Note: Alternatively you could call super's -didSelectPost, which will similarly complete the extension context.
        print("Completing requests")
    }

    override func configurationItems() -> [Any]! {
        // To add configuration options via table cells at the bottom of the sheet, return an array of SLComposeSheetConfigurationItem here.
        return []
    }

}

extension FileManager {
  static func sharedContainerURL() -> URL {
    return FileManager.default.containerURL(
      forSecurityApplicationGroupIdentifier: "group.synesthesia.ReaderApp"
    )!
  }
}
