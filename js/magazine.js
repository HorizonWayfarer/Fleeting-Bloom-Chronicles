/*
 * Magazine sample with PDF.js integration
 */

var pdfDocument = null;
var totalPages = 0;
var renderedPages = {};
var thumbnailCache = {};
var isMobile = false;

function setMobileMode(value) {
    isMobile = value;
}

function isMobileDevice() {
    if (typeof window === 'undefined') return false;
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
           (window.innerWidth <= 768);
}

function initPDF(pdfUrl, callback) {
    if (pdfDocument) {
        if (callback) callback(pdfDocument);
        return;
    }
    
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'js/pdf.worker.min.js';
    
    pdfjsLib.getDocument({
        url: pdfUrl,
        cMapUrl: 'https://unpkg.com/pdfjs-dist@3.11.174/cmaps/',
        cMapPacked: true
    }).promise.then(function(pdf) {
        pdfDocument = pdf;
        totalPages = pdf.numPages;
        
        if (callback) callback(pdf);
    }).catch(function(error) {
        console.error('PDF loading error:', error);
        if (callback) callback(null, error);
    });
}

function renderPDFPage(pageNum, container, scale) {
    if (!pdfDocument) return;
    
    pdfDocument.getPage(pageNum).then(function(page) {
        var viewport = page.getViewport({ scale: scale || 1 });
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        
        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        
        page.render(renderContext).promise.then(function() {
            var shadowClass = pageNum % 2 === 0 ? 'shadow-right' : 'shadow-left';
            $(container).html('<img src="' + canvas.toDataURL('image/png') + '" style="width:100%;height:100%;" /><div class="shadow ' + shadowClass + '"></div><div class="gradient"></div>');
            renderedPages[pageNum] = canvas.toDataURL('image/png');
        });
    });
}

function generateThumbnail(pageNum, width, height, callback) {
    if (thumbnailCache[pageNum]) {
        if (callback) callback(thumbnailCache[pageNum]);
        return;
    }
    
    if (!pdfDocument) return;
    
    pdfDocument.getPage(pageNum).then(function(page) {
        var viewport = page.getViewport({ scale: 0.2 });
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        
        canvas.width = width || 76;
        canvas.height = height || 100;
        
        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        
        page.render(renderContext).promise.then(function() {
            var dataUrl = canvas.toDataURL('image/png');
            thumbnailCache[pageNum] = dataUrl;
            if (callback) callback(dataUrl);
        });
    });
}

function updateLoadingProgress(completed, total) {
    var progress = Math.round((completed / total) * 100);
    $('#loading').text('正在加载杂志... ' + progress + '%');
}

function generateAllThumbnails(callback) {
    if (!pdfDocument) {
        initPDF('pages/magazine.pdf', function() {
            generateAllThumbnails(callback);
        });
        return;
    }
    
    var completed = 0;
    updateLoadingProgress(0, totalPages);
    for (var i = 1; i <= totalPages; i++) {
        generateThumbnail(i, 76, 100, function() {
            completed++;
            updateLoadingProgress(completed, totalPages);
            if (completed === totalPages && callback) {
                callback();
            }
        });
    }
}

function addPage(page, book) {
    var id, pages = book.turn('pages');
    var element = $('<div />', {});

    if (book.turn('addPage', element, page)) {
        var shadowClass = page % 2 === 0 ? 'shadow-right' : 'shadow-left';
        element.html('<div class="gradient"></div><div class="loader"></div><div class="shadow ' + shadowClass + '"></div>');
        loadPage(page, element);
    }
}

function loadPage(page, pageElement) {
    var shadowClass = page % 2 === 0 ? 'shadow-right' : 'shadow-left';
    
    if (renderedPages[page]) {
        pageElement.html('<img src="' + renderedPages[page] + '" style="width:100%;height:100%;" /><div class="shadow ' + shadowClass + '"></div><div class="gradient"></div>');
        return;
    }
    
    if (!pdfDocument) {
        initPDF('pages/magazine.pdf', function() {
            renderPDFPage(page, pageElement, 1);
        });
    } else {
        renderPDFPage(page, pageElement, 1);
    }
    
    loadRegions(page, pageElement);
}

function loadLargePage(page, pageElement) {
    if (!pdfDocument) {
        initPDF('pages/magazine.pdf', function() {
            renderPDFPage(page, pageElement, 2);
        });
    } else {
        renderPDFPage(page, pageElement, 2);
    }
}

function loadSmallPage(page, pageElement) {
    if (!pdfDocument) {
        initPDF('pages/magazine.pdf', function() {
            renderPDFPage(page, pageElement, 1);
        });
    } else {
        renderPDFPage(page, pageElement, 1);
    }
}

function loadRegions(page, element) {
}

function addRegion(region, pageElement) {
    var reg = $('<div />', {'class': 'region  ' + region['class']}),
        options = $('.magazine').turn('options'),
        pageWidth = options.width/2,
        pageHeight = options.height;

    reg.css({
        top: Math.round(region.y/pageHeight*100)+'%',
        left: Math.round(region.x/pageWidth*100)+'%',
        width: Math.round(region.width/pageWidth*100)+'%',
        height: Math.round(region.height/pageHeight*100)+'%'
    }).attr('region-data', $.param(region.data||''));

    reg.appendTo(pageElement);
}

function regionClick(event) {
    var region = $(event.target);

    if (region.hasClass('region')) {
        $('.magazine-viewport').data().regionClicked = true;
        
        setTimeout(function() {
            $('.magazine-viewport').data().regionClicked = false;
        }, 100);
        
        var regionType = $.trim(region.attr('class').replace('region', ''));
        return processRegion(region, regionType);
    }
}

function processRegion(region, regionType) {
    data = decodeParams(region.attr('region-data'));

    switch (regionType) {
        case 'link' :
            window.open(data.url);
            break;
        case 'zoom' :
            var regionOffset = region.offset(),
                viewportOffset = $('.magazine-viewport').offset(),
                pos = {
                    x: regionOffset.left-viewportOffset.left,
                    y: regionOffset.top-viewportOffset.top
                };
            $('.magazine-viewport').zoom('zoomIn', pos);
            break;
        case 'to-page' :
            $('.magazine').turn('page', data.page);
            break;
    }
}

function zoomTo(event) {
    setTimeout(function() {
        if ($('.magazine-viewport').data().regionClicked) {
            $('.magazine-viewport').data().regionClicked = false;
        } else {
            if ($('.magazine-viewport').zoom('value')==1) {
                $('.magazine-viewport').zoom('zoomIn', event);
            } else {
                $('.magazine-viewport').zoom('zoomOut');
            }
        }
    }, 1);
}

function isChrome() {
    return navigator.userAgent.indexOf('Chrome')!=-1;
}

function disableControls(page) {
    if (page==1)
        $('.previous-button').hide();
    else
        $('.previous-button').show();
                
    if (page==$('.magazine').turn('pages'))
        $('.next-button').hide();
    else
        $('.next-button').show();
}

function resizeViewport() {
    var width = $(window).width(),
        height = $(window).height(),
        options = $('.magazine').turn('options');

    $('.magazine').removeClass('animated');

    $('.magazine-viewport').css({
        width: width,
        height: height
    }).zoom('resize');

    if ($('.magazine').turn('zoom')==1) {
        var bound = calculateBound({
            width: options.width,
            height: options.height,
            boundWidth: Math.min(options.width, width),
            boundHeight: Math.min(options.height, height)
        });

        if (bound.width%2!==0)
            bound.width-=1;

        if (bound.width!=$('.magazine').width() || bound.height!=$('.magazine').height()) {
            $('.magazine').turn('size', bound.width, bound.height);

            if ($('.magazine').turn('page')==1)
                $('.magazine').turn('peel', 'br');

            $('.next-button').css({height: bound.height, backgroundPosition: '-38px '+(bound.height/2-32/2)+'px'});
            $('.previous-button').css({height: bound.height, backgroundPosition: '-4px '+(bound.height/2-32/2)+'px'});
        }

        $('.magazine').css({top: -bound.height/2, left: -bound.width/2});
    }

    var magazineOffset = $('.magazine').offset(),
        boundH = height - magazineOffset.top - $('.magazine').height(),
        marginTop = (boundH - $('.thumbnails > div').height()) / 2;

    if (marginTop<0) {
        $('.thumbnails').css({height:1});
    } else {
        $('.thumbnails').css({height: boundH});
        $('.thumbnails > div').css({marginTop: marginTop});
    }

    if (magazineOffset.top<$('.made').height())
        $('.made').hide();
    else
        $('.made').show();

    $('.magazine').addClass('animated');
}

function numberOfViews(book) {
    return book.turn('pages') / 2 + 1;
}

function getViewNumber(book, page) {
    return parseInt((page || book.turn('page'))/2 + 1, 10);
}

function largeMagazineWidth() {
    return 2214;
}

function decodeParams(data) {
    var parts = data.split('&'), d, obj = {};

    for (var i =0; i<parts.length; i++) {
        d = parts[i].split('=');
        obj[decodeURIComponent(d[0])] = decodeURIComponent(d[1]);
    }

    return obj;
}

function calculateBound(d) {
    var bound = {width: d.width, height: d.height};

    if (bound.width>d.boundWidth || bound.height>d.boundHeight) {
        var rel = bound.width/bound.height;

        if (d.boundWidth/rel>d.boundHeight && d.boundHeight*rel<=d.boundWidth) {
            bound.width = Math.round(d.boundHeight*rel);
            bound.height = d.boundHeight;
        } else {
            bound.width = d.boundWidth;
            bound.height = Math.round(d.boundWidth/rel);
        }
    }
        
    return bound;
}

function buildThumbnails() {
    var thumbnails = $('.thumbnails ul');
    thumbnails.empty();
    
    var li;
    
    if (isMobile) {
        for (var i = 1; i <= totalPages; i++) {
            li = $('<li class="i"></li>');
            var img = $('<img width="76" height="100" class="page-' + i + '">');
            img.attr('src', thumbnailCache[i] || '');
            li.append(img);
            li.append('<span>' + i + '</span>');
            thumbnails.append(li);
        }
    } else {
        for (var i = 1; i <= totalPages; i++) {
            if (i === 1) {
                li = $('<li class="i"></li>');
                var img = $('<img width="76" height="100" class="page-' + i + '">');
                img.attr('src', thumbnailCache[i] || '');
                li.append(img);
                li.append('<span>' + i + '</span>');
                thumbnails.append(li);
            } else if (i % 2 === 0 && i < totalPages) {
                li = $('<li class="d"></li>');
                var img1 = $('<img width="76" height="100" class="page-' + i + '">');
                img1.attr('src', thumbnailCache[i] || '');
                var img2 = $('<img width="76" height="100" class="page-' + (i+1) + '">');
                img2.attr('src', thumbnailCache[i+1] || '');
                li.append(img1);
                li.append(img2);
                li.append('<span>' + i + '-' + (i+1) + '</span>');
                thumbnails.append(li);
            }
        }
        
        if (totalPages % 2 === 0) {
            li = $('<li class="i"></li>');
            var lastImg = $('<img width="76" height="100" class="page-' + totalPages + '">');
            lastImg.attr('src', thumbnailCache[totalPages] || '');
            li.append(lastImg);
            li.append('<span>' + totalPages + '</span>');
            thumbnails.append(li);
        }
    }
}