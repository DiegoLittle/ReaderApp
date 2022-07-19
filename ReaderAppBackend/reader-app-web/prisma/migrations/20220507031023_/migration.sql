/*
  Warnings:

  - The primary key for the `bookmarks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `uuid` on the `bookmarks` table. All the data in the column will be lost.
  - The required column `id` was added to the `bookmarks` table with a prisma-level default value. This is not possible if the table is not empty. Please add this column as optional, then populate it before making it required.

*/
-- DropIndex
DROP INDEX "ix_bookmarks_uuid";

-- AlterTable
ALTER TABLE "bookmarks" DROP CONSTRAINT "bookmarks_pkey",
DROP COLUMN "uuid",
ADD COLUMN     "id" VARCHAR NOT NULL,
ADD CONSTRAINT "bookmarks_pkey" PRIMARY KEY ("id");

-- CreateIndex
CREATE INDEX "ix_bookmarks_id" ON "bookmarks"("id");
