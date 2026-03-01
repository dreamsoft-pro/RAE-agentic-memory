import React, { useEffect, useRef, useState } from 'react';
import UserPagePreview from '../UserPagePreview';
import { connect, useSelector } from 'react-redux';
import { toggleViews, togglePages } from '../../redux/actions/carousel';

const CarouselBox = ({ editor, container, isViewsOpen, isPagesOpen, toggleViews, togglePages }) => {
  const viewsListContentRef = useRef(null);
  const pagesListContentRef = useRef(null);
  const viewsListUserRef = useRef(null);
  const pagesListUserRef = useRef(null);
  const topPagesListUserRef = useRef(null);

  const selectTodos = (state) => state.templatesReducer; 

        // const returnedTodos = useSelector(selectTodos);

        // console.log("STORE:",returnedTodos);

  const updateTopPagesPosition = () => {
    if (topPagesListUserRef.current) {
      if (!isViewsOpen && !isPagesOpen) {
        topPagesListUserRef.current.style.transform = 'translateY(110px)';
      } else {
        topPagesListUserRef.current.style.transform = 'translateY(0)';
      }
    }
  };

  const handleScroll = (ref, direction) => {
    if (ref.current) {
      ref.current.scrollLeft += direction * 240;
      Ps.update(ref.current);
    }
  };

  const handleAddPageClick = (e) => {
    e.stopPropagation();

    const proj = editor.userProject.getObj().projects[editor.userProject.getObj().projects.length - 1];
    // TODO - Update logic to avoid assuming the last project is always the target.

    if (editor.checkPagesCountConstraint({ project: proj, addRemove: 'ADD' })) {
      let pos = editor.userProject.getCurrentView().order + 1;
      if (pos === proj.Views.length) {
        pos--;
      }
      editor.webSocketControllers.userProject.addNewView(proj._id, pos);
    }
  };

  const handleApplyPage = (e) => {
    e.stopPropagation();            
    const selectedTheme = document.querySelector('.userThemePage.selected')

    if (selectedTheme) {
        const pages = editor.stage.getPages();

        if(!pages.length) {
            return;
        }
        
        editor.webSocketControllers.userPage.useThemePage(editor.stage.getPages()[0].userPage._id, selectedTheme.getAttribute('theme-page-id'), function (data) {
            store.dispatch(updateTemplatesData(data.themePage.proposedTemplates));
            editor.stage.getPages()[0].loadThemePage(data.themePage);
            editor.stage.getPages()[0].loadTemplate(data.proposedTemplate, data.usedImages);
        });

        selectedTheme.classList.remove('selected');

    }
  }

  const handleApplyAllPages = (e) => {
    e.stopPropagation();            
    const selectedTheme = document.querySelector('.userThemePage.selected')

    if (selectedTheme) {
        const pages = editor.stage.getPages();
        // console.log(store.state)

        if(!pages.length) {
            return;
        }
        
        console.log("STORE:", store.getState())
        editor.webSocketControllers.userPage.useThemePage(editor.stage.getPages()[0].userPage._id, selectedTheme.getAttribute('theme-page-id'), function (data) {
            store.dispatch(updateTemplatesData(data.themePage.proposedTemplates));
            editor.stage.getPages()[0].loadThemePage(data.themePage);
            editor.stage.getPages()[0].loadTemplate(data.proposedTemplate, data.usedImages);
        });

        selectedTheme.classList.remove('selected');

    }
  }

  const handleSort = (e) => {
      e.stopPropagation();
      editor.template.displayAllPagesWithPhotos();
  };

  useEffect(() => {
    
    updateTopPagesPosition();

    if (viewsListContentRef.current) {
      Ps.initialize(viewsListContentRef.current, { useBothWheelAxes: true });
    }
    if (pagesListContentRef.current) {
      Ps.initialize(pagesListContentRef.current, { useBothWheelAxes: true });
    }

    const handleResize = () => {
      if (viewsListUserRef.current && viewsListContentRef.current) {
        const width = viewsListUserRef.current.offsetWidth - 200;
        viewsListContentRef.current.style.width = `${width}px`;
      }
      if (pagesListUserRef.current && pagesListContentRef.current) {
        const width = pagesListUserRef.current.offsetWidth - 200;
        pagesListContentRef.current.style.width = `${width}px`;
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => {
      if (viewsListContentRef.current) Ps.destroy(viewsListContentRef.current);
      if (pagesListContentRef.current) Ps.destroy(pagesListContentRef.current);
      window.removeEventListener('resize', handleResize);
    };
  }, [isViewsOpen, isPagesOpen]);

  return (
    <div id="carouselBox" className="carouselBox">
      {/* Views List */}

      <div id="topPagesListUser" ref={topPagesListUserRef}>
          <div className="currentPagesSwitcher">
              <div className="pagesControllers">
              <div className="prevPage" onClick={() => editor.userProject.turnToPreviousView()} />
              <div className="currentPageInfo" />
              <div className="pagesInfo" />
              <div className="nextPage" onClick={() => editor.userProject.turnToNextView()} />
              </div>
          </div>
          {/* Pages List Header */}
          <div
              className={`pagesListHeader ${isPagesOpen ? 'active' : ''}`}
              onClick={togglePages}>
          </div>
          {/* Views List Label */}
          <div
          className={`viewsListLabel ${isViewsOpen ? 'active' : ''}`}
          onClick={toggleViews}
          >
          </div>
      </div>

      <div
        id="viewsListUser"
        className={`displayController ${isViewsOpen ? 'open' : 'closed'}`}
      >
        {/* Main Buttons */}
        <div id="mainViewsButtons">
          <div id="addPageButton" className="actionButton" onClick={(e) => handleAddPageClick(e)}>
            <span id="addPageButtonDesc" className="actionButtonDesc">Dodaj strone</span>
          </div>
          <div id="allPagesPopUpButton" className="actionButton" onClick={(e) => handleSort(e)}>
            <span id="allPagesPopUpButtonDesc" className="actionButtonDesc">Sortuj</span>
          </div>
        </div>

        {/* Scroll Buttons */}
        <div
          id="scrollViewsLeft"
          className="scrollButton"
          onClick={() => handleScroll(viewsListContentRef, -1)}
        />
        <div
          className="viewsListContent"
          ref={viewsListContentRef}
        >
        <UserPagePreview editor={editor} container={container} />
        </div>
        <div
          id="scrollViewsRight"
          className="scrollButton"
          onClick={() => handleScroll(viewsListContentRef, 1)}
        />
      </div>

      {/* Pages List */}
      <div
        id="pagesListUser"
        className={`displayController ${isPagesOpen ? 'open' : 'closed'}`}
      >
        {/* Bottom Section */}
        <div id="bottomPagesListUser">
          <div id="pageListButtons">
            <div id="applyPageButton" className="actionButton" onClick={(e) => handleApplyPage(e)}>
              <span id="applyPageButtonDesc" className="actionButtonDesc">Zastosuj dla strony</span>
            </div>
            <div id="applyAllPagesButton" className="actionButton">
              <span id="applyAllPagesButtonDesc" className="actionButtonDesc">Dla wszystkich stron</span>
            </div>
          </div>
          <div
            id="scrollThemesLeft"
            className="scrollButton"
            onClick={() => handleScroll(pagesListContentRef, -1)}
          />
          <div className="pagesListContent" ref={pagesListContentRef} />
          <div
            id="scrollThemesRight"
            className="scrollButton"
            onClick={() => handleScroll(pagesListContentRef, 1)}
          />
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = (state) =>  ({
    isViewsOpen: state.carouselReducer.isViewsOpen,
    isPagesOpen: state.carouselReducer.isPagesOpen,
});

const mapDispatchToProps = (dispatch) => ({
  toggleViews: () => dispatch(toggleViews()),
  togglePages: () => dispatch(togglePages()),
});

export default connect(mapStateToProps, mapDispatchToProps)(CarouselBox);
