//
//  JournalEntry.swift
//  Journal
//
//  Created by Diego Little on 10/16/21.
//

import Foundation
import RealmSwift
import SwiftUI


//class NoteListItem: Object {
//    var _id: UUID = NSUUID() as UUID
//    var title: String = ""
//    var body: String = ""
//}

final class NoteListItem: Object, ObjectKeyIdentifiable,Codable {
    /// The unique ID of the Item. `primaryKey: true` declares the
    /// _id member as the primary key to the realm.
    @Persisted(primaryKey: true) var _id: ObjectId
    /// The name of the Item, By default, a random name is generated.
    @Persisted var title:String
    /// A flag indicating whether the user "favorited" the item.
    @Persisted var body=""
    /// The backlink to the `Group` this item is a part of.
    ///     enum CodingKeys: String, CodingKey {
    enum CodingKeys: String, CodingKey {
    case _id
    }

    func encode(to encoder: Encoder) throws {
    var container = encoder.container(keyedBy: CodingKeys.self)
    try container.encode(_id, forKey: ._id)
    }
}


//final class NoteList: Object, ObjectKeyIdentifiable {
//    /// The unique ID of the Group. `primaryKey: true` declares the
//    /// _id member as the primary key to the realm.
//    @Persisted(primaryKey: true) var _id: ObjectId
//    /// The collection of Items in this group.
//    @Persisted var items = RealmSwift.List<NoteListItem>()
//}
