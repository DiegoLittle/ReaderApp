//
//  NoteViewModel.swift
//  Journal
//
//  Created by Diego Little on 11/20/21.
//

import Foundation
import Alamofire
import RealmSwift



class NoteViewModel: ObservableObject{
    
    @Published var note:NoteListItem;
    @Published var title="";
    @Published var body="";
    @Published var _id:ObjectId;
    
    init(_ note: NoteListItem = NoteListItem()){
        print(note)
        self.note = note;
        self.title = note.title
        self.body = note.body
        self._id = note._id

//        guard note.isInvalidated == false else {
//            return
//           // The object has been deleted, so dismiss this view controller
//        }

    }

//    @Published var title = "";
//    @Published var body = "";
    
    func postNote() {
//        let test = realm.objects(NoteListItem.self).first!

        let my_note = NoteListItem(value: ["_id":self._id,"title": self.title, "body": self.body])

        let realm = try! Realm()

        
        try! realm.write {
            // Add the instance to the realm.
            realm.add(my_note, update:.all)
        }
        let token: String = UserDefaults.standard.string(forKey: "access_token") ?? ""
        let encoder = JSONEncoder()
        let myResults = realm.object(ofType: NoteListItem.self, forPrimaryKey: my_note._id)!
//        print(note)
        print("Realm object result: ")
        print(myResults)
//        let myResults = realm.objects(note.self)

        let jsonNote = try! String(data: encoder.encode(myResults), encoding: .utf8)!
//        let jsonNote = try! encoder.encode(note);
        let access_token = ["access_token": token]
//        let parameters = ["token":access_token,"note":String(data:jsonNote,encoding: .utf8)!] as [String : Any]
        let parameters = ["token":access_token,"note":jsonNote] as [String : Any]
        
        let finalBody = try! JSONSerialization.data(withJSONObject: parameters)
        let url = URL(string: "http://127.0.0.1:5000/user/notes")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = finalBody
        let task = URLSession.shared.dataTask(with: request) { data, response, error in            
//            print(response)
//            print(String(data: data, encoding: .utf8)!)
        }.resume()
        print(parameters)
    }
    
}
