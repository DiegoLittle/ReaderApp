//
//  Models.swift
//  ReaderApp
//
//  Created by Diego Little on 4/30/22.
//

import Foundation
import SwiftUI
import Fuse

struct Bookmark: Identifiable, Equatable,Codable, Fuseable{
    var id:UUID = UUID()
    var url:String? = ""
    var title:String? = ""
    var type:String? = "web"
    var description:String? = ""
    
    var properties: [FuseProperty] {
        return [
            FuseProperty(name: "title", weight: 1),
        ]
    }
}
