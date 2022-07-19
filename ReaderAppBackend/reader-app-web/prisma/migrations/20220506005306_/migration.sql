/*
  Warnings:

  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `bookmarks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `bookmarks` table. All the data in the column will be lost.
  - You are about to drop the `Account` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Session` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `VerificationToken` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `items` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `notes` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `uuid` to the `bookmarks` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Account" DROP CONSTRAINT "Account_userId_fkey";

-- DropForeignKey
ALTER TABLE "Session" DROP CONSTRAINT "Session_userId_fkey";

-- DropIndex
DROP INDEX "ix_bookmarks_id";

-- AlterTable
ALTER TABLE "User" DROP CONSTRAINT "User_pkey",
ALTER COLUMN "id" SET DATA TYPE VARCHAR,
ALTER COLUMN "name" SET DATA TYPE VARCHAR,
ALTER COLUMN "email" SET DATA TYPE VARCHAR,
ALTER COLUMN "emailVerified" SET DATA TYPE TIMESTAMP(6),
ALTER COLUMN "image" SET DATA TYPE VARCHAR,
ADD CONSTRAINT "User_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "bookmarks" DROP CONSTRAINT "bookmarks_pkey",
DROP COLUMN "id",
ADD COLUMN     "owner_id" VARCHAR,
ADD COLUMN     "uuid" VARCHAR NOT NULL,
ADD CONSTRAINT "bookmarks_pkey" PRIMARY KEY ("uuid");

-- DropTable
DROP TABLE "Account";

-- DropTable
DROP TABLE "Session";

-- DropTable
DROP TABLE "VerificationToken";

-- DropTable
DROP TABLE "items";

-- DropTable
DROP TABLE "notes";

-- CreateIndex
CREATE INDEX "ix_bookmarks_uuid" ON "bookmarks"("uuid");

-- AddForeignKey
ALTER TABLE "bookmarks" ADD CONSTRAINT "bookmarks_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "User"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- RenameIndex
ALTER INDEX "User_email_key" RENAME TO "ix_User_email";

-- RenameIndex
ALTER INDEX "ix_users_id" RENAME TO "ix_User_id";
