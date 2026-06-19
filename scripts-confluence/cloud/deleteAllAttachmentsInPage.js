/*
How to use
1. Copy all the code from the snippet.
2. On Chrome browser bookmarks bar, right-click and Add Page.
3. Enter any Name that you wish.
4. In the URL box paste the copied code and save.
5. On a Confluence page’s attachment section - click the bookmark to run.

Code below
*/
  
javascript:
function main() {
    var pageID = document.location.href.split('?pageId=')[1];
    if (pageID.includes('&')) {
        var pageID = pageID.split('&')[0];
    }
    const urls = [`${document.location.origin}/wiki/rest/api/content/${pageID}/child/attachment`];
    const attIDs = [];
    const repo = [];
    const count = [0];
    const cols = ['No.', 'Attachment ID', 'Title', 'Type', 'Media Type', 'Status', 'Space'];

    const createTableCols = (cols, row, tableName) => {
        cols.forEach((e) => {
            cell = document.createElement('th');
            cell.innerHTML = e;
            cell.style.fontFamily = 'Helvetica';
            cell.style.textAlign = 'center';
            cell.bgColor = '#0063cc';
            cell.style.color = '#ffffff';
            cell.border = '1';
            row.appendChild(cell);
        });
        tableName.appendChild(row);
    };

    function td(x, row, y, space) {
        var y = y || 0;
        var space = space || 0;
        var cell = document.createElement('td');
        if (y) {
            cell.innerHTML = `${x}`;
        }
        else {
            cell.innerHTML = x;
        }
        cell.style.fontFamily = 'Helvetica';
        cell.style.textAlign = 'center';
        row.appendChild(cell);
    };

    async function deleteIds() {
        var rows = document.getElementsByTagName('tr');
    for (i=1; i< rows.length; i++) {
        if (rows[i].cells[1].innerText != 'Id to AttId') {
            const id = rows[i].cells[1].innerText;
            const spacekey = rows[i].cells[6].innerText;
            const response = await fetch(`${document.location.origin}/wiki/rest/api/content/${id}`, {method:'DELETE'});
            rows[i].cells[5].innerHTML = `Trashed`;
            const cell1 = document.createElement('td');
            const cell2 = document.createElement('td');
            cell1.innerHTML = `<a href=${document.location.origin}/wiki/pages/restoretrashitem.action?key=${spacekey}&contentId=${id} target=_blank>Restore</a>`;
            cell2.innerHTML = `<a href=${document.location.origin}/wiki/pages/purgetrashitem.action?key=${spacekey}&contentId=${id} target=_blank>Purge</a>`;
            rows[i].appendChild(cell1);
            rows[i].appendChild(cell2);
            }
        }
    document.getElementById("delBtn").disabled = true;
    };

    const gen = () => {
        var purgeTable = document.createElement('table');
        var row0 = document.createElement('tr');
        createTableCols(cols, row0, purgeTable);
        return purgeTable
    };

    const fetchData = async (purgeTable) => {
        while(true) {
                const url = `${urls[0]}`;
                const response = await fetch(url).then((r) => (r.json() ));
                console.log(response.results);
                response.results.map(ele => {
                    const attid = ele.id.replace(/\\D/g, '');
                    const title = ele.title;
                    const type = ele.type;
                    const mediaType = ele.metadata.mediaType;
                    const filetype = mediaType.split('/')[1];
                    const status = ele.status;
                    const space = ele._expandable.space.split('/rest/api/space/')[1];
                    const indx = count[0] + 1;
                    count.pop();
                    count.push(indx);
                    attIDs.push(attid);
                    repo.push(attid, title, type, mediaType, status, space);
                    const row = document.createElement('tr');
                    td(indx, row);
                    td(attid, row);
                    td(title, row);
                    td(type, row);
                    td(mediaType, row);
                    td(status, row);
                    td(space, row);
                    if ( indx % 2 == 1) {
                        row.bgColor = '#e6e6ff';
                        }
                    purgeTable.appendChild(row);
                    });
                if ( response._links.hasOwnProperty('next') == true ) {
                    urls.pop();
                    const next = `${document.location.origin}/wiki${response._links.next}`;
                    urls.push(next);
                }
                if ( response._links.hasOwnProperty('next') == false ) {
                    urls.pop();
                    var para1 = document.createElement('p');
                    var para2 = document.createElement('p');
                    para1.appendChild(purgeTable);
                    const btn1 = document.createElement('button');
                    btn1.setAttribute('id', 'delBtn');
                    btn1.innerText = 'DELETE ALL';
                    const sc1 = document.createElement('script');
                    sc1.innerHTML = deleteIds;
                    btn1.setAttribute('onclick', 'deleteIds()');
                    para2.appendChild(sc1);
                    para2.appendChild(btn1);
                    para1.appendChild(para2);
                    return para1;
                }
        }
    };

    const writeReport = (data) => {
            var mywin = window.open('_blank');
            mywin.document.write(data.innerHTML);
    };

    const purgeTable = gen();
    fetchData(purgeTable).then(writeReport);
}

var ans = confirm("Once deleted, attachment(s) will need to be purged, are you sure you want to continue?");
    if(ans == true) {
        main();
    }
